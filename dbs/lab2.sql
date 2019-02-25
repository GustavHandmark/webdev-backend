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

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    title           TEXT NOT NULL,
    prod_year       INTEGER NOT NULL,
    imdb_id         TEXT NOT NULL,
    PRIMARY KEY (imdb_id)
    );

DROP TABLE IF EXISTS theaters;
CREATE TABLE theaters (
    t_name      TEXT NOT NULL,
    capacity    INTEGER NOT NULL CHECK (capacity > 0),
    PRIMARY KEY (t_name)
    );

DROP TABLE IF EXISTS performances;
CREATE TABLE performances (
    p_id              TEXT DEFAULT (lower(hex(randomblob(16)))),
    imdb_id         TEXT NOT NULL,
    t_name          TEXT NOT NULL,
    date            DATE NOT NULL,
    time            TIME NOT NULL,
    PRIMARY KEY (p_id),
    FOREIGN KEY (imdb_id) REFERENCES movies(imdb_id),
    FOREIGN KEY (t_name) REFERENCES theaters(t_name)
    );

DROP TABLE IF EXISTS tickets;
CREATE TABLE tickets (
    id          TEXT DEFAULT (lower(hex(randomblob(16)))),
    username    TEXT NOT NULL,
    p_id        TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (p_id) REFERENCES performances(p_id)
    );

-- Insert data into the tables
INSERT
INTO users(username, u_name, password) 
VALUES  ('kallecool', 'Karl Lagerfeld','hej123'),
        ('snyggErik','Erik Segerstedt','1234'),
        ('jsson','Albin Johansson','password'),
        ('heaton','Emil Christensen','password'),
        ('snurresprett','Lille Skutt','password');


INSERT 
INTO movies(title, prod_year,imdb_id)
VALUES  ('Interstellar',2014,'tt0816692'),
        ('The Shawnshank Redemption',1994, 'tt0111161'),
        ('Pulp Fiction', 1994, 'tt0110912'),
        ('The Room', 2003, 'tt0368226'),
        ('The Disaster Artist', 2017, 'tt3521126'),
        ('The Prestige', 2006, 'tt0482571'),
        ('Justin Bieber: Never Say Never',2011, 'tt1702443');

INSERT 
INTO theaters(t_name, capacity)
VALUES  ('SF LUND', 250),
        ('SF MALMÖ', 350),
        ('Eksjö biograf', 75);

PRAGMA foreign_keys=ON;
