CREATE TABLE events (
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,             -- 'TechHeads 2026'
    starts_at  DATE
);

CREATE TABLE keywords (
    term TEXT NOT NULL
    id        SERIAL PRIMARY KEY,
    event_id  INT NOT NULL REFERENCES events(id),
     -- 'techheads', '#techheads', 'tech heads'
);

CREATE TABLE sources (
    id      SERIAL PRIMARY KEY,
    kind    TEXT NOT NULL,                -- 'telegram', 'vk', 'synthetic'
    handle  TEXT,                         -- @канал или id группы
    title   TEXT
);

CREATE TABLE personas (
    id           SERIAL PRIMARY KEY,
    age          INT,
    gender       TEXT,
    region       TEXT,
    occupation   TEXT,
    ocean        JSONB,                   -- черты личности
    description  TEXT
);

CREATE TABLE raw_messages (
    id           SERIAL PRIMARY KEY,
    source_id    INT NOT NULL REFERENCES sources(id),
    external_id  TEXT,                    -- id сообщения в источнике
    author       TEXT,
    text         TEXT NOT NULL,
    posted_at    TIMESTAMPTZ,
    fetched_at   TIMESTAMPTZ DEFAULT now(),
    UNIQUE (source_id, external_id)       -- защита от дублей при повторном сборе
);

CREATE TABLE mentions (
    id              SERIAL PRIMARY KEY,
    raw_message_id  INT NOT NULL REFERENCES raw_messages(id),
    event_id        INT NOT NULL REFERENCES events(id),
    persona_id      INT REFERENCES personas(id),   -- только для синтетики
    sentiment       TEXT,                          -- заполним позже
    topics          TEXT[],
    is_synthetic    BOOLEAN DEFAULT false
);