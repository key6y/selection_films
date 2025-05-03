CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE directors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE series (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    release_year INT,
    rating FLOAT,
    seasons INT,
    director_id INT REFERENCES directors(id),
    country VARCHAR(100),
    language VARCHAR(50),
    age_rating VARCHAR(10)
);

CREATE TABLE series_genres (
    series_id INT REFERENCES series(id),
    genre_id INT REFERENCES genres(id),
    PRIMARY KEY (series_id, genre_id)
);

CREATE TABLE series_actors (
    series_id INT REFERENCES series(id),
    actor_id INT REFERENCES actors(id),
    PRIMARY KEY (series_id, actor_id)
);

-- Вставка начальных данных
INSERT INTO genres (name) VALUES ('Драма'), ('Комедия'), ('Фантастика');
INSERT INTO actors (name) VALUES ('Эмилия Кларк'), ('Брайан Крэнстон');
INSERT INTO directors (name) VALUES ('Дэвид Бениофф');
INSERT INTO series (title, release_year, rating, seasons, director_id, country, language, age_rating)
VALUES ('Игра престолов', 2011, 9.3, 8, 1, 'США', 'Английский', '18+');
INSERT INTO series_genres (series_id, genre_id) VALUES (1, 1), (1, 3);
INSERT INTO series_actors (series_id, actor_id) VALUES (1, 1);