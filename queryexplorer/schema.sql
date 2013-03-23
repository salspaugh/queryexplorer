DROP TABLE IF EXISTS queries;
CREATE TABLE queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    time REAL,
    user INTEGER REFERENCES users(id),
    session INTEGER REFERENCES sessions(id),
    CONSTRAINT issuing_user FOREIGN KEY (user) REFERENCES users(id),
    CONSTRAINT containing_session FOREIGN KEY (session) REFERENCES session(id)
);

drop table if exists users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT
);

drop table if exists sessions;
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user INTEGER REFERENCES users(id),
    CONSTRAINT owner FOREIGN KEY (user) REFERENCES users(id)
);
