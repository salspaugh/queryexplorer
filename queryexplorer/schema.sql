DROP TABLE IF EXISTS queries;
CREATE TABLE queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    time REAL,
    type TEXT,
    user INTEGER REFERENCES users(id),
    session INTEGER REFERENCES sessions(id),
    CONSTRAINT issuing_user FOREIGN KEY (user) REFERENCES users(id),
    CONSTRAINT containing_session FOREIGN KEY (session) REFERENCES session(id)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT
);

DROP TABLE IF EXISTS sessions;
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user INTEGER REFERENCES users(id),
    type text,
    CONSTRAINT owner FOREIGN KEY (user) REFERENCES users(id)
);

DROP TABLE IF EXISTS commands_indicators;
CREATE TABLE commands_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_vector TEXT NOT NULL,
    query INTEGER REFERENCES queries(id),
    CONSTRAINT corresponding_query FOREIGN KEY (query) REFERENCES queries(id)
);

DROP TABLE IF EXISTS commands_indicator_key;
CREATE TABLE commands_indicator_key (
    command TEXT PRIMARY KEY,
    idx INTEGER NOT NULL
);
