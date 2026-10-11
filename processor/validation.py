
from datetime import datetime

REQUIRED_FIELDS = (
    "source_name",
    "source_event_id",
    "name",
    "venue",
    "date",
    "source_updated_at",
)


def validate_record(record):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"Missing required field: {field}")
        else:
            if not isinstance(record[field], str) or not record[field].strip():
                errors.append(f"Field '{field}' must be a non-empty string.")
            elif field == "date":
                try:
                    parsed_date = datetime.strptime(record[field], "%Y-%m-%d")
                    formatted_date = parsed_date.strftime("%Y-%m-%d")
                    if formatted_date != record[field]:
                        errors.append(f"Field '{field}' must be a valid date in YYYY-MM-DD format.")
                except ValueError:
                    errors.append(f"Field '{field}' must be a valid date in YYYY-MM-DD format.")
    return errors
