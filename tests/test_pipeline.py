
from generator.dataset import generate_records
from processor.pipeline import prepare_record
from processor.deduplication import build_event_key

def test_valid_record_is_normalized():
    record = generate_records()[1]
    result = prepare_record(record)

    assert result["status"] == "valid"
    assert result["normalized_record"]["name"] == "jazz night"
    assert result["normalized_record"]["venue"] == "blue hall"
    assert result["errors"] == []
    assert record["name"] == " Jazz Night "


def test_invalid_record_is_quarantined():
    record = generate_records()[5]
    result = prepare_record(record)

    assert result["status"] == "quarantined"
    assert result["normalized_record"] is None
    assert result["raw_record"]["date"] == ""
    assert result["errors"]