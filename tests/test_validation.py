
from generator.dataset import generate_records
from processor.validation import validate_record


def test_valid_record_passes():
    record = generate_records()[0]
    errors = validate_record(record)
    assert not errors

def test_missing_date_is_rejected():
    record = generate_records()[0].copy()
    record["date"] = ""

    assert "Field 'date' must be a non-empty string." in validate_record(record)

def test_impossible_date_is_rejected():
    record = generate_records()[0].copy()
    record["date"] = "2026-02-30"

    assert "Field 'date' must be a valid date in YYYY-MM-DD format." in validate_record(record)

def test_non_padded_date_is_rejected():
    record = generate_records()[0].copy()
    record["date"] = "2026-1-2"

    assert "Field 'date' must be a valid date in YYYY-MM-DD format." in validate_record(record)