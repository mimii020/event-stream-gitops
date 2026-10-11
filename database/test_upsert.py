
from database.connection import get_connection
from database.repository import (
    get_or_create_event_id,
    upsert_source_record,
)

conn = get_connection()

try:
    blue_event = {
        "name": "test concert",
        "venue": "blue hall",
        "date": "2026-12-01",
    }
    green_event = {
        "name": "test concert",
        "venue": "green hall",
        "date": "2026-12-01",
    }

    blue_id = get_or_create_event_id(blue_event, conn)
    green_id = get_or_create_event_id(green_event, conn)

    original = {
        "source_name": "TEST",
        "source_event_id": "TEST-001",
        "source_updated_at": "2026-10-10T14:05:00Z",
    }

    upsert_source_record(original, blue_id, conn)

    corrected = {
        **original,
        "source_updated_at": "2026-10-10T15:00:00Z",
    }
    upsert_source_record(corrected, green_id, conn)

    stale = {
        **original,
        "source_updated_at": "2026-10-10T14:30:00Z",
    }
    upsert_source_record(stale, blue_id, conn)

    row = conn.execute(
        """
        SELECT event_id, source_updated_at
        FROM source
        WHERE source_name = %s
          AND source_event_id = %s
        """,
        ("TEST", "TEST-001"),
    ).fetchone()

    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM source
        WHERE source_name = %s
          AND source_event_id = %s
        """,
        ("TEST", "TEST-001"),
    ).fetchone()[0]

    assert row[0] == green_id
    assert row[1].hour == 15
    assert count == 1

    print("Source upsert test passed!")
    print("Current event ID:", row[0])
    print("Stored update time:", row[1])

finally:
    conn.rollback()
    conn.close()
