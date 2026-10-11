from database.connection import get_connection
from database.repository import (
    persist_valid_records,
    persist_quarantined_records,
)
from generator.dataset import generate_records
from processor.pipeline import process_records


def main():
    records = generate_records()
    results = process_records(records)

    with get_connection() as conn:
        persist_valid_records(results, conn)
        persist_quarantined_records(results, conn)

        event_count = conn.execute(
            "SELECT COUNT(*) FROM canonical_events"
        ).fetchone()[0]

        source_count = conn.execute(
            "SELECT COUNT(*) FROM source"
        ).fetchone()[0]

        quarantine_count = conn.execute(
            "SELECT COUNT(*) FROM quarantined"
        ).fetchone()[0]

        print("Quarantined records:", quarantine_count)
        print("Canonical events:", event_count)
        print("Source records:", source_count)

    assert event_count == 4, f"Expected 4 events, got {event_count}"
    assert source_count == 5, f"Expected 5 source records, got {source_count}"
    assert quarantine_count == 1, f"Expected 1 quarantined record, got {quarantine_count}"

    print("Persistence check passed!")


if __name__ == "__main__":
    main()
