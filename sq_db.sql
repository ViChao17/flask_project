CREATE TABLE IF NOT EXISTS mainmenu(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS user (
	id	INTEGER UNIQUE,
	name TEXT,
	info TEXT,
	login TEXT NOT NULL UNIQUE,
	pass INTEGER NOT NULL,
	register_date INTEGER
	PRIMARY KEY(id AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS article (
	id	INTEGER UNIQUE,
	title TEXT NOT NULL,
	text TEXT,
	author_id INTEGER,
	PRIMARY KEY(id AUTOINCREMENT),
	FOREIGN KEY(author_id) REFERENCES user(id) ON DELETE SET NULL
);