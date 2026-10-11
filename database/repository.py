from psycopg.types.json import Jsonb

def get_or_create_event_id(event, conn):
    conn.execute(
        """
        INSERT INTO canonical_events (event_name, event_venue, event_date)
        VALUES (%s, %s, %s)
        ON CONFLICT (event_name, event_venue, event_date) DO NOTHING
        """,
        (event["name"].strip(), event["venue"].strip(), event["date"]),
    )

    row = conn.execute(
        """
        SELECT id FROM canonical_events
        WHERE event_name = %s AND event_venue = %s AND event_date = %s
        """,
        (event["name"].strip(), event["venue"].strip(), event["date"]),
    ).fetchone()

    if row is None:
        raise RuntimeError("Failed to retrieve event ID.")
    
    return row[0]

def upsert_source_record(record, canonical_event_id, conn):
    conn.execute(
        """
        INSERT INTO source (source_name, source_event_id, source_updated_at, event_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (source_name, source_event_id) DO UPDATE
        SET source_updated_at = EXCLUDED.source_updated_at,
            event_id = EXCLUDED.event_id
        WHERE source.source_updated_at < EXCLUDED.source_updated_at
        """,
        (
            record["source_name"],
            record["source_event_id"],
            record["source_updated_at"],
            canonical_event_id,
        ),
    )

def persist_valid_records(results, conn):
    event_ids_by_key = {}

    for event_key, event in results["canonical_events"].items():
        event_id = get_or_create_event_id(event, conn)
        event_ids_by_key[event_key] = event_id

    for record in results["source_records"]:
        event_key = record["event_key"]
        event_id = event_ids_by_key[event_key]
        upsert_source_record(record, event_id, conn)
        
    conn.execute(
        """
        DELETE FROM canonical_events AS e
        WHERE NOT EXISTS (
            SELECT 1
            FROM source AS s
            WHERE s.event_id = e.id
        )
        """
    )

def persist_quarantined_records(results, conn):
    for item in results["quarantined"]:
        raw_record = item["raw_record"]
        errors = item["errors"]

        source_id = None
        source_name = raw_record.get("source_name")
        source_event_id = raw_record.get("source_event_id")

        if (
            isinstance(source_name, str)
            and source_name.strip()
            and isinstance(source_event_id, str)
            and source_event_id.strip()
        ):
            row = conn.execute(
                """
                SELECT id
                FROM source
                WHERE source_name = %s
                  AND source_event_id = %s
                """,
                (source_name, source_event_id),
            ).fetchone()

            if row is not None:
                source_id = row[0]

        conn.execute(
            """
            INSERT INTO quarantined (source_id, raw_record, errors)
            VALUES (%s, %s, %s)
            ON CONFLICT (raw_record, errors) DO NOTHING
            """,
            (source_id, Jsonb(raw_record), Jsonb(errors)),
        )