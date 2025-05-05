-- Создание таблицы жанров
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Создание таблицы актёров
CREATE TABLE actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Создание таблицы режиссёров
CREATE TABLE directors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Создание таблицы сериалов
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

-- Создание таблицы связи сериалов и жанров
CREATE TABLE series_genres (
    series_id INT REFERENCES series(id),
    genre_id INT REFERENCES genres(id),
    PRIMARY KEY (series_id, genre_id)
);

-- Создание таблицы связи сериалов и актёров
CREATE TABLE series_actors (
    series_id INT REFERENCES series(id),
    actor_id INT REFERENCES actors(id),
    PRIMARY KEY (series_id, actor_id)
);

-- Создание таблицы фильмов
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INTEGER NOT NULL,
    country VARCHAR(100) NOT NULL,
    language VARCHAR(50) NOT NULL,
    age_rating VARCHAR(10) NOT NULL,
    rating NUMERIC(3,1),
    duration INTEGER NOT NULL,
    director_id INTEGER,
    CONSTRAINT movies_rating_check CHECK (rating >= 0 AND rating <= 10),
    CONSTRAINT movies_director_id_fkey FOREIGN KEY (director_id) REFERENCES directors(id) ON DELETE SET NULL
);

-- Создание таблицы связи фильмов и жанров
CREATE TABLE movie_genres (
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

-- Создание таблицы связи фильмов и актёров
CREATE TABLE movie_actors (
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    actor_id INTEGER REFERENCES actors(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, actor_id)
);

-- Вставка начальных данных

-- Жанры
INSERT INTO genres (name) VALUES
    ('Драма'),
    ('Комедия'),
    ('Фантастика'),
    ('Триллер'),
    ('Боевик');

-- Актёры
INSERT INTO actors (name) VALUES
    ('Эмилия Кларк'),
    ('Брайан Крэнстон'),
    ('Джессика Честейн'),
    ('Том Харди');

-- Режиссёры
INSERT INTO directors (name) VALUES
    ('Дэвид Бениофф'),
    ('Винс Гиллиган'),
    ('Кристофер Нолан'),
    ('Джеймс Кэмерон'),
    ('Стивен Спилберг'),
    ('Ридли Скотт'),
    ('Квентин Тарантино'),
    ('Мартин Скорсезе'),
    ('Дэвид Финчер'),
    ('Алехандро Гонсалес Иньярриту'),
    ('Кристофер МакКуорри'),
    ('Дени Вильнёв'),
    ('Лана Вачовски'),
    ('Питер Джексон'),
    ('Роберт Земекис');

-- Сериалы
INSERT INTO series (title, release_year, rating, seasons, director_id, country, language, age_rating) VALUES
    ('Игра престолов', 2011, 9.3, 8, (SELECT id FROM directors WHERE name='Дэвид Бениофф'), 'США', 'Английский', '18+'),
    ('Во все тяжкие', 2008, 9.5, 5, (SELECT id FROM directors WHERE name='Винс Гиллиган'), 'США', 'Английский', '18+'),
    ('Начало', 2010, 8.8, 1, (SELECT id FROM directors WHERE name='Кристофер Нолан'), 'США', 'Английский', '16+');

-- Связи сериалов с жанрами
INSERT INTO series_genres (series_id, genre_id) VALUES
    ((SELECT id FROM series WHERE title='Игра престолов'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM series WHERE title='Игра престолов'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM series WHERE title='Во все тяжкие'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM series WHERE title='Во все тяжкие'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM series WHERE title='Начало'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM series WHERE title='Начало'), (SELECT id FROM genres WHERE name='Боевик'));

-- Связи сериалов с актёрами
INSERT INTO series_actors (series_id, actor_id) VALUES
    ((SELECT id FROM series WHERE title='Игра престолов'), (SELECT id FROM actors WHERE name='Эмилия Кларк')),
    ((SELECT id FROM series WHERE title='Во все тяжкие'), (SELECT id FROM actors WHERE name='Брайан Крэнстон')),
    ((SELECT id FROM series WHERE title='Начало'), (SELECT id FROM actors WHERE name='Джессика Честейн')),
    ((SELECT id FROM series WHERE title='Начало'), (SELECT id FROM actors WHERE name='Том Харди'));

-- Фильмы
INSERT INTO movies (title, release_year, country, language, age_rating, rating, duration, director_id) VALUES
    ('Начало', 2010, 'США', 'Английский', '12+', 8.8, 148, (SELECT id FROM directors WHERE name='Кристофер Нолан')),
    ('Интерстеллар', 2014, 'США', 'Английский', '12+', 8.6, 169, (SELECT id FROM directors WHERE name='Кристофер Нолан')),
    ('Престиж', 2006, 'США', 'Английский', '16+', 8.5, 130, (SELECT id FROM directors WHERE name='Кристофер Нолан')),
    ('Однажды в Голливуде', 2019, 'США', 'Английский', '18+', 7.6, 161, (SELECT id FROM directors WHERE name='Квентин Тарантино')),
    ('Джанго освобождённый', 2012, 'США', 'Английский', '18+', 8.4, 165, (SELECT id FROM directors WHERE name='Квентин Тарантино')),
    ('Бесславные ублюдки', 2009, 'США', 'Английский', '18+', 8.3, 153, (SELECT id FROM directors WHERE name='Квентин Тарантино')),
    ('Волк с Уолл-стрит', 2013, 'США', 'Английский', '18+', 8.2, 180, (SELECT id FROM directors WHERE name='Мартин Скорсезе')),
    ('Отступники', 2006, 'США', 'Английский', '18+', 8.5, 151, (SELECT id FROM directors WHERE name='Мартин Скорсезе')),
    ('Казино', 1995, 'США', 'Английский', '18+', 8.2, 178, (SELECT id FROM directors WHERE name='Мартин Скорсезе')),
    ('Аватар', 2009, 'США', 'Английский', '12+', 7.8, 162, (SELECT id FROM directors WHERE name='Джеймс Кэмерон')),
    ('Титаник', 1997, 'США', 'Английский', '12+', 7.8, 194, (SELECT id FROM directors WHERE name='Джеймс Кэмерон')),
    ('Терминатор 2: Судный день', 1991, 'США', 'Английский', '18+', 8.5, 137, (SELECT id FROM directors WHERE name='Джеймс Кэмерон')),
    ('Список Шиндлера', 1993, 'США', 'Английский', '16+', 8.9, 195, (SELECT id FROM directors WHERE name='Стивен Спилберг')),
    ('Инопланетянин', 1982, 'США', 'Английский', '6+', 7.9, 115, (SELECT id FROM directors WHERE name='Стивен Спилберг')),
    ('Парк Юрского периода', 1993, 'США', 'Английский', '12+', 8.1, 127, (SELECT id FROM directors WHERE name='Стивен Спилберг')),
    ('Социальная сеть', 2010, 'США', 'Английский', '16+', 7.7, 120, (SELECT id FROM directors WHERE name='Дэвид Финчер')),
    ('Исчезнувшая', 2014, 'США', 'Английский', '18+', 8.1, 149, (SELECT id FROM directors WHERE name='Дэвид Финчер')),
    ('Выживший', 2015, 'США', 'Английский', '18+', 8.0, 156, (SELECT id FROM directors WHERE name='Алехандро Гонсалес Иньярриту')),
    ('Птичка', 2014, 'США', 'Английский', '18+', 8.1, 119, (SELECT id FROM directors WHERE name='Алехандро Гонсалес Иньярриту')),
    ('Миссия невыполнима: Племя изгоев', 2015, 'США', 'Английский', '16+', 7.4, 131, (SELECT id FROM directors WHERE name='Кристофер МакКуорри')),
    ('Миссия невыполнима: Последствия', 2018, 'США', 'Английский', '16+', 7.7, 147, (SELECT id FROM directors WHERE name='Кристофер МакКуорри')),
    ('Дюна', 2021, 'США', 'Английский', '12+', 8.1, 155, (SELECT id FROM directors WHERE name='Дени Вильнёв')),
    ('Прибытие', 2016, 'США', 'Английский', '12+', 7.9, 116, (SELECT id FROM directors WHERE name='Дени Вильнёв')),
    ('Джентльмены', 2019, 'Великобритания', 'Английский', '18+', 8.1, 113, (SELECT id FROM directors WHERE name='Гай Ричи')),
    ('Бойцовский клуб', 1999, 'США', 'Английский', '18+', 8.8, 139, (SELECT id FROM directors WHERE name='Дэвид Финчер')),
    ('Храброе сердце', 1995, 'США', 'Английский', '16+', 8.3, 178, (SELECT id FROM directors WHERE name='Мэл Гибсон')),
    ('Криминальное чтиво', 1994, 'США', 'Английский', '18+', 8.9, 154, (SELECT id FROM directors WHERE name='Квентин Тарантино')),
    ('Матрица', 1999, 'США', 'Английский', '16+', 8.7, 136, (SELECT id FROM directors WHERE name='Лана Вачовски')),
    ('Гладиатор', 2000, 'США', 'Английский', '16+', 8.5, 155, (SELECT id FROM directors WHERE name='Ридли Скотт')),
    ('Властелин колец: Возвращение короля', 2003, 'Новая Зеландия', 'Английский', '12+', 8.9, 201, (SELECT id FROM directors WHERE name='Питер Джексон')),
    ('Человек из стали', 2013, 'США', 'Английский', '12+', 7.0, 143, (SELECT id FROM directors WHERE name='Зак Снайдер')),
    ('Форрест Гамп', 1994, 'США', 'Английский', '12+', 8.8, 142, (SELECT id FROM directors WHERE name='Роберт Земекис')),
    ('Марсианин', 2015, 'США', 'Английский', '12+', 8.0, 144, (SELECT id FROM directors WHERE name='Ридли Скотт')),
    ('Бешеные псы', 1992, 'США', 'Английский', '18+', 8.3, 99, (SELECT id FROM directors WHERE name='Квентин Тарантино')),
    ('Остров проклятых', 2010, 'США', 'Английский', '18+', 8.2, 138, (SELECT id FROM directors WHERE name='Мартин Скорсезе')),
    ('Спасти рядового Райана', 1998, 'США', 'Английский', '18+', 8.6, 169, (SELECT id FROM directors WHERE name='Стивен Спилберг')),
    ('Тёмный рыцарь', 2008, 'США', 'Английский', '12+', 9.0, 152, (SELECT id FROM directors WHERE name='Кристофер Нолан')),
    ('Челюсти', 1975, 'США', 'Английский', '16+', 8.0, 124, (SELECT id FROM directors WHERE name='Стивен Спилберг'));

-- Связи фильмов с жанрами
INSERT INTO movie_genres (movie_id, genre_id) VALUES
    ((SELECT id FROM movies WHERE title='Начало'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Начало'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Интерстеллар'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Престиж'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM movies WHERE title='Однажды в Голливуде'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Джанго освобождённый'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Джанго освобождённый'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Бесславные ублюдки'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Бесславные ублюдки'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Волк с Уолл-стрит'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Отступники'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM movies WHERE title='Казино'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Аватар'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Титаник'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Терминатор 2: Судный день'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Терминатор 2: Судный день'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Список Шиндлера'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Инопланетянин'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Парк Юрского периода'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Социальная сеть'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Исчезнувшая'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM movies WHERE title='Выживший'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Выживший'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Птичка'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM movies WHERE title='Миссия невыполнима: Племя изгоев'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Миссия невыполнима: Последствия'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Миссия невыполнима: Последствия'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM movies WHERE title='Дюна'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Прибытие'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Джентльмены'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Бойцовский клуб'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Храброе сердце'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Храброе сердце'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Криминальное чтиво'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Криминальное чтиво'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Матрица'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Матрица'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Гладиатор'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Гладиатор'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Властелин колец: Возвращение короля'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Человек из стали'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Форрест Гамп'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Марсианин'), (SELECT id FROM genres WHERE name='Фантастика')),
    ((SELECT id FROM movies WHERE title='Бешеные псы'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM movies WHERE title='Остров проклятых'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM movies WHERE title='Спасти рядового Райана'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Спасти рядового Райана'), (SELECT id FROM genres WHERE name='Драма')),
    ((SELECT id FROM movies WHERE title='Тёмный рыцарь'), (SELECT id FROM genres WHERE name='Боевик')),
    ((SELECT id FROM movies WHERE title='Тёмный рыцарь'), (SELECT id FROM genres WHERE name='Триллер')),
    ((SELECT id FROM movies WHERE title='Челюсти'), (SELECT id FROM genres WHERE name='Триллер'));

-- Связи фильмов с актёрами (добавлены примерные данные)
INSERT INTO movie_actors (movie_id, actor_id) VALUES
    ((SELECT id FROM movies WHERE title='Начало'), (SELECT id FROM actors WHERE name='Джессика Честейн')),
    ((SELECT id FROM movies WHERE title='Интерстеллар'), (SELECT id FROM actors WHERE name='Джессика Честейн')),
    ((SELECT id FROM movies WHERE title='Тёмный рыцарь'), (SELECT id FROM actors WHERE name='Том Харди')),
    ((SELECT id FROM movies WHERE title='Матрица'), (SELECT id FROM actors WHERE name='Том Харди'));