    CREATE TABLE canonical_events (
        id SERIAL PRIMARY KEY,
        event_name TEXT NOT NULL,
        event_venue TEXT NOT NULL,
        event_date DATE NOT NULL,
        UNIQUE(event_name, event_venue, event_date)
    );

    CREATE TABLE source (
        id SERIAL PRIMARY KEY,
        source_name TEXT NOT NULL,
        source_event_id TEXT NOT NULL,
        source_updated_at TIMESTAMPTZ NOT NULL,
        event_id INT REFERENCES canonical_events(id) NOT NULL,
        UNIQUE(source_name, source_event_id)
    );

    CREATE TABLE quarantined (
        id SERIAL PRIMARY KEY,
        source_id INT REFERENCES source(id),
        raw_record JSONB NOT NULL,
        errors JSONB NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );