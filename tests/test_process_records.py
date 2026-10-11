from generator.dataset import generate_records
from processor.pipeline import process_records


def find_source_record(results, source_name, source_event_id):
    return next(
        record
        for record in results["source_records"]
        if record["source_name"] == source_name
        and record["source_event_id"] == source_event_id
    )


def test_duplicate_sources_share_canonical_event():
    results = process_records(generate_records())

    source_a = find_source_record(results, "A", "A-104")
    source_b = find_source_record(results, "B", "B-892")

    assert source_a["event_key"] == source_b["event_key"]

    assert len(results["canonical_events"]) == 4


def test_different_dates_create_separate_events():
    results = process_records(generate_records())

    source_a = find_source_record(results, "A", "A-104")
    source_c = find_source_record(results, "C", "D-77")

    assert source_a["event_key"] != source_c["event_key"]

    assert source_a["event_key"] == (
        "jazz night",
        "blue hall",
        "2026-11-12",
    )
    assert source_c["event_key"] == (
        "jazz night",
        "blue hall",
        "2026-11-13",
    )


def test_repeated_delivery_is_preserved_for_database_upsert():
    record = generate_records()[0]

    results = process_records([record, record.copy()])

    assert len(results["source_records"]) == 2

    first, second = results["source_records"]

    assert first["source_name"] == second["source_name"]
    assert first["source_event_id"] == second["source_event_id"]
    assert first["source_updated_at"] == second["source_updated_at"]
    assert first["event_key"] == second["event_key"]

    assert len(results["canonical_events"]) == 1


def test_process_records_counts():
    results = process_records(generate_records())

    assert len(results["canonical_events"]) == 4
    assert len(results["source_records"]) == 5
    assert len(results["quarantined"]) == 1


def test_invalid_record_is_quarantined_without_losing_raw_input():
    invalid_record = generate_records()[-1]

    results = process_records([invalid_record])

    assert len(results["quarantined"]) == 1

    quarantined = results["quarantined"][0]

    assert quarantined["status"] == "quarantined"
    assert quarantined["raw_record"] == invalid_record
    assert any(
        "date" in error.lower()
        for error in quarantined["errors"]
    )
