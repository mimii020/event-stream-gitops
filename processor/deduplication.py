

def build_event_key(record):
    return (record["name"], record["venue"], record["date"])