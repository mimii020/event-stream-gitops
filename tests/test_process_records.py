
from generator.dataset import generate_records
from processor.pipeline import process_records


def test_expected_processing_counts():
    result = process_records(generate_records())

    assert len(result["canonical_events"]) == 4, f"Expected 4 canonical events, got {len(result['canonical_events'])}"
    assert len(result["source_records"]) == 5, f"Expected 5 source records, got {len(result['source_records'])}"
    assert len(result["quarantined"]) == 1, f"Expected 1 quarantined record, got {len(result['quarantined'])}"


def test_duplicate_sources_share_canonical_event():
    result = process_records(generate_records())

    source_a = result["source_records"][("A-104", "A")]
    source_b = result["source_records"][("B-892", "B")]

    assert source_a["event_id"] == source_b["event_id"]

def test_different_dates_create_separate_events():
    result = process_records(generate_records())

    source_a = result["source_records"][("A-104", "A")]
    source_c = result["source_records"][("D-77", "C")]

    assert source_a["event_id"] != source_c["event_id"]



def test_invalid_record_is_quarantined():
    result = process_records(generate_records())

    assert len(result["quarantined"]) == 1

    quarantined = result["quarantined"][0]

    assert quarantined["status"] == "quarantined"
    assert quarantined["raw_record"]["date"] == ""
    assert quarantined["normalized_record"] is None
    assert quarantined["errors"]
    assert any("date" in error.lower() for error in quarantined["errors"])

def test_repeated_delivery_does_not_duplicate_records():
    record = generate_records()[0]

    result = process_records([record, record.copy()])

    assert len(result["canonical_events"]) == 1, f"Expected 1 canonical event, got {len(result['canonical_events'])}"
    assert len(result["source_records"]) == 1, f"Expected 1 source record, got {len(result['source_records'])}"
    assert len(result["quarantined"]) == 0, f"Expected 0 quarantined records, got {len(result['quarantined'])}"