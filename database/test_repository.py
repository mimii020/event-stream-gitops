
from database.connection import get_connection
from database.repository import get_or_create_event_id


event = {
    "name": "jazz night",
    "venue": "blue hall",
    "date": "2026-11-12",
}

with get_connection() as conn:
    first_id = get_or_create_event_id(event, conn)
    second_id = get_or_create_event_id(event, conn)

    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM canonical_events
        WHERE event_name = %s
          AND event_venue = %s
          AND event_date = %s
        """,
        (event["name"], event["venue"], event["date"]),
    ).fetchone()[0]

    print("First ID:", first_id)
    print("Second ID:", second_id)
    print("Matching rows:", count)

    assert first_id == second_id
    assert count == 1

print("Repository test passed!")
