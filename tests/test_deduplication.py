from generator.dataset import generate_records
from processor.pipeline import prepare_record

def test_deduplication():
    records = generate_records()
    results = [prepare_record(record) for record in records]
    record1 = results[0]
    record2 = results[1]
    record3 = results[2]

    assert record1["status"] == "valid"
    assert record2["status"] == "valid"
    assert record3["status"] == "valid"

    assert record1["event_key"] == record2["event_key"]
    assert record1["event_key"] != record3["event_key"]