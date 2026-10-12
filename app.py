from generator.dataset import generate_records
from processor.pipeline import process_records
from database.connection import get_connection
from database.repository import (
    persist_valid_records,
    persist_quarantined_records,
)

def main():
    with get_connection() as conn:
        records = generate_records()
        results = process_records(records)
        persist_valid_records(results, conn)
        persist_quarantined_records(results, conn)

        print("Canonical events persisted:", len(results["canonical_events"]))
        print("Source records persisted:", len(results["source_records"]))
        print("Quarantined records persisted:", len(results["quarantined"]))

if __name__ == "__main__":
    main()