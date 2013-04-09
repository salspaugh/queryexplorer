DROP TABLE IF EXISTS queries_commands_indicator_groups;
CREATE TABLE queries_commands_indicator_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class TEXT,
    commands_indicator_group_id INTEGER
);

DROP TABLE IF EXISTS commands_indicators;
CREATE TABLE commands_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_vector TEXT NOT NULL,
    query_id INTEGER REFERENCES queries(id),
    CONSTRAINT corresponding_query FOREIGN KEY (query_id) REFERENCES queries(id)
);

DROP TABLE IF EXISTS commands_indicator_key;
CREATE TABLE commands_indicator_key (
    command TEXT PRIMARY KEY,
    idx INTEGER NOT NULL
);

DROP TABLE IF EXISTS commands_indicator_coordinates;
CREATE TABLE commands_indicator_coordinates (
    rowidx INTEGER NOT NULL,
    colidx INTEGER NOT NULL,
    command TEXT,
    hash TEXT UNIQUE,
    class TEXT,
    indicator_group_id INTEGER
);
