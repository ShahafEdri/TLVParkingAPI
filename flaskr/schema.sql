DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS parking_info;
DROP TABLE IF EXISTS parking_tonnage;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE parking_info (
  parking_id INTEGER UNIQUE PRIMARY KEY,
  parking_name_iw TEXT NOT NULL,
  parking_address_iw TEXT NOT NULL,
  parking_name_en TEXT NOT NULL,
  parking_address_en TEXT NOT NULL,
  parking_latitute TEXT NOT NULL,
  parking_longitute TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parking_tonnage (
  parking_id INTEGER PRIMARY KEY,
  parking_tonnage TEXT NOT NULL,
  last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (parking_id) REFERENCES parking_info (parking_id)
);