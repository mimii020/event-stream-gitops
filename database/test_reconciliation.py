from database.connection import get_connection
from database.repository import persist_valid_records
from processor.pipeline import process_records


records = [
    {
        "source_name": "RECON-FINAL",
        "source_event_id": "RECON-001",
        "name": "Reconciliation Demo",
        "venue": "Green Hall",
        "date": "2026-12-02",
        "source_updated_at": "2026-10-10T15:00:00Z",
    },
    {
        "source_name": "RECON-FINAL",
        "source_event_id": "RECON-001",
        "name": "Reconciliation Demo",
        "venue": "Blue Hall",
        "date": "2026-12-02",
        "source_updated_at": "2026-10-10T14:00:00Z",
    },
]

conn = get_connection()

try:
    results = process_records(records)
    persist_valid_records(results, conn)

    row = conn.execute(
        """
        SELECT e.event_venue, s.source_updated_at
        FROM source AS s
        JOIN canonical_events AS e ON e.id = s.event_id
        WHERE s.source_name = %s
          AND s.source_event_id = %s
        """,
        ("RECON-FINAL", "RECON-001"),
    ).fetchone()

    event_count = conn.execute(
        """
        SELECT COUNT(*)
        FROM canonical_events
        WHERE event_name = %s
          AND event_date = %s
        """,
        ("reconciliation demo", "2026-12-02"),
    ).fetchone()[0]

    print("Selected venue:", row[0] if row else None)
    print("Selected update:", row[1] if row else None)
    print("Canonical events for this test:", event_count)

    assert row is not None
    assert row[0] == "green hall"
    assert row[1].hour == 15
    assert event_count == 1

    print("Same-batch reconciliation passed!")

finally:
    conn.rollback()
    conn.close()
