-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;


-- create the tables.
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username    TEXT NOT NULL,
    u_name      TEXT NOT NULL,
    password    TEXT NOT NULL, -- some check to ensure it's hashed?
    PRIMARY KEY (username)
    );

DROP TABLE IF EXISTS recipes;
CREATE TABLE recipes (
    recipe_id   TEXT DEFAULT (lower(hex(randomblob(16)))),
    ingredients TEXT NOT NULL,
    directions  TEXT NOT NULL,
    title       TEXT NOT NULL,
    recipe_url  TEXT NOT NULL,
    PRIMARY KEY(recipe_id)
);
-- Insert data into the tables
INSERT
INTO users(username, u_name, password) 
VALUES  ('kallecool', 'Karl Lagerfeld','hej123'),
        ('snyggErik','Erik Segerstedt','1234'),
        ('jsson','Albin Johansson','password'),
        ('heaton','Emil Christensen','password'),
        ('snurresprett','Lille Skutt','password');

PRAGMA foreign_keys=ON;
