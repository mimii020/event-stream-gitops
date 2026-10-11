from processor.normalization import normalize_record
from processor.validation import validate_record
from processor.deduplication import build_event_key
import uuid

def prepare_record(record):
    raw_record = record.copy()

    errors = validate_record(raw_record)

    if errors:
        return {
            "status": "quarantined",
            "raw_record": raw_record,
            "normalized_record": None,
            "errors": errors,
        }
    else:
        normalized_record = normalize_record(raw_record)
        event_key = build_event_key(normalized_record)
        return {
            "status": "valid",
            "raw_record": raw_record,
            "normalized_record": normalized_record,
            "event_key": event_key,
            "errors": []
        }

def process_records(records):
    canonical_events = {}
    source_records = {}
    quarantined = []

    for record in records:
        results = prepare_record(record)
        if results["status"] == "quarantined":
            quarantined.append(results)
        elif results["status"] == "valid":
            event_key = results["event_key"]
            normalized_record = results["normalized_record"]
            if event_key not in canonical_events:
                unique_id = uuid.uuid4()
                id_str = str(unique_id)
                canonical_events[event_key] = {
                    "id": id_str,
                    "name": normalized_record["name"],
                    "venue": normalized_record["venue"],
                    "date": normalized_record["date"]
                }

            source_event_id = normalized_record["source_event_id"]
            source_name = normalized_record["source_name"]
            source_updated_at = normalized_record["source_updated_at"]
            event_id = canonical_events[event_key]["id"]
            source_key = (source_event_id, source_name)
            source_records[source_key] = {
                "source_name": source_name,
                "source_event_id": source_event_id,
                "source_updated_at": source_updated_at,
                "event_id": event_id
            }
    return {
        "canonical_events": canonical_events,
        "source_records": source_records,
        "quarantined": quarantined
    }
