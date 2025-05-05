import psycopg2

class ExpertSystem:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_recommendations(self, content_type="all", genre=None, min_rating=0, year_from=None, year_to=None, country=None, language=None, age_rating=None, director=None, actor=None, min_seasons=None, max_seasons=None, sort_by="rating", limit=10):
        query = "SELECT title, release_year, rating, seasons, duration FROM ("
        if content_type in ["series", "all"]:
            query += "SELECT s.title, s.release_year, s.rating, s.seasons, NULL as duration FROM series s "
            if genre:
                query += "JOIN series_genres sg ON s.id = sg.series_id JOIN genres g ON sg.genre_id = g.id WHERE g.name = %s "
            else:
                query += "WHERE 1=1 "
            if min_rating:
                query += f"AND s.rating >= {min_rating} "
            if year_from:
                query += f"AND s.release_year >= {year_from} "
            if year_to:
                query += f"AND s.release_year <= {year_to} "
            if country:
                query += f"AND s.country = '{country}' "
            if language:
                query += f"AND s.language = '{language}' "
            if age_rating:
                query += f"AND s.age_rating = '{age_rating}' "
            if director:
                query += f"JOIN directors d ON s.director_id = d.id WHERE d.name = '{director}' "
            if actor:
                query += f"JOIN series_actors sa ON s.id = sa.series_id JOIN actors a ON sa.actor_id = a.id WHERE a.name = '{actor}' "
            if min_seasons is not None:
                query += f"AND s.seasons >= {min_seasons} "
            if max_seasons is not None:
                query += f"AND s.seasons <= {max_seasons} "
        if content_type == "all":
            query += " UNION "
        if content_type in ["movie", "all"]:
            query += "SELECT m.title, m.release_year, m.rating, NULL as seasons, m.duration FROM movies m "
            if genre:
                query += "JOIN movie_genres mg ON m.id = mg.movie_id JOIN genres g ON mg.genre_id = g.id WHERE g.name = %s "
            else:
                query += "WHERE 1=1 "
            if min_rating:
                query += f"AND m.rating >= {min_rating} "
            if year_from:
                query += f"AND m.release_year >= {year_from} "
            if year_to:
                query += f"AND m.release_year <= {year_to} "
            if country:
                query += f"AND m.country = '{country}' "
            if language:
                query += f"AND m.language = '{language}' "
            if age_rating:
                query += f"AND m.age_rating = '{age_rating}' "
            if director:
                query += f"JOIN directors d ON m.director_id = d.id WHERE d.name = '{director}' "
            if actor:
                query += f"JOIN movie_actors ma ON m.id = ma.movie_id JOIN actors a ON ma.actor_id = a.id WHERE a.name = '{actor}' "
        query += ") AS results "
        if sort_by == "rating":
            query += "ORDER BY rating DESC "
        elif sort_by == "year":
            query += "ORDER BY release_year DESC "
        elif sort_by == "seasons":
            query += "ORDER BY seasons DESC "
        query += f"LIMIT {limit}"
        params = (genre,) if genre else ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_genres(self, title, is_movie):
        table = "movies" if is_movie else "series"
        self.cursor.execute(f"""
            SELECT g.name
            FROM {table} t
            JOIN {'movie' if is_movie else 'series'}_genres tg ON t.id = tg.{'movie' if is_movie else 'series'}_id
            JOIN genres g ON tg.genre_id = g.id
            WHERE t.title = %s
        """, (title,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_director(self, title, is_movie):
        table = "movies" if is_movie else "series"
        self.cursor.execute(f"""
            SELECT d.name
            FROM {table} t
            JOIN directors d ON t.director_id = d.id
            WHERE t.title = %s
        """, (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_country(self, title, is_movie):
        table = "movies" if is_movie else "series"
        self.cursor.execute(f"SELECT country FROM {table} WHERE title = %s", (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_language(self, title, is_movie):
        table = "movies" if is_movie else "series"
        self.cursor.execute(f"SELECT language FROM {table} WHERE title = %s", (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_age_rating(self, title, is_movie):
        table = "movies" if is_movie else "series"
        self.cursor.execute(f"SELECT age_rating FROM {table} WHERE title = %s", (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def view_available_options(self):
        print("\n=== Доступные варианты ===")
        self.cursor.execute("SELECT name FROM genres")
        genres = [row[0] for row in self.cursor.fetchall()]
        print(f"Жанры: {', '.join(genres)}")
        self.cursor.execute("SELECT name FROM actors")
        actors = [row[0] for row in self.cursor.fetchall()]
        print(f"Актёры: {', '.join(actors)}")
        self.cursor.execute("SELECT name FROM directors")
        directors = [row[0] for row in self.cursor.fetchall()]
        print(f"Режиссёры: {', '.join(directors)}")