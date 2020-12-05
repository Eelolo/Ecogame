DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_items;

CREATE TABLE items(
    item_id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER
);

CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    credits INTEGER DEFAULT 450
);

CREATE TABLE user_items(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    item_id INTEGER
);

INSERT INTO users(username, password, credits) VALUES('Admin', 'pbkdf2:sha256:150000$yi41916K$16a522be739b189bbc0d0f1dae7882cbe63c9ef0172a71db4ce72fe506536fd1', 100500);

		