

def normalize_record(record):
    normalized_record = record.copy()
    for field in ("name", "venue"):
        value = normalized_record[field]
        if isinstance(value, str):
            normalized_record[field] = " ".join(value.lower().split())
    return normalized_record