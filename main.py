import psycopg2

class ExpertSystem:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_recommendations(self, content_type="all", genre=None, min_rating=0, year_from=None, year_to=None, country=None, language=None, age_rating=None, director=None, actor=None, min_seasons=None, max_seasons=None, sort_by="rating", limit=10):
        query = "SELECT title, release_year, rating, seasons, duration FROM ("
        params = []
        if content_type in ["series", "all"]:
            query += "SELECT s.title, s.release_year, s.rating, s.seasons, NULL as duration FROM series s "
            joins = []
            where_clauses = ["1=1"]
            if genre:
                joins.append("JOIN series_genres sg ON s.id = sg.series_id JOIN genres g ON sg.genre_id = g.id")
                where_clauses.append("LOWER(g.name) = %s")
                params.append(genre)
            if min_rating:
                where_clauses.append("s.rating >= %s")
                params.append(min_rating)
            if year_from:
                where_clauses.append("s.release_year >= %s")
                params.append(year_from)
            if year_to:
                where_clauses.append("s.release_year <= %s")
                params.append(year_to)
            if country:
                where_clauses.append("LOWER(s.country) = %s")
                params.append(country)
            if language:
                where_clauses.append("LOWER(s.language) = %s")
                params.append(language)
            if age_rating:
                where_clauses.append("s.age_rating = %s")
                params.append(age_rating)
            if director:
                joins.append("JOIN directors d ON s.director_id = d.id")
                where_clauses.append("LOWER(d.name) = %s")
                params.append(director)
            if actor:
                joins.append("JOIN series_actors sa ON s.id = sa.series_id JOIN actors a ON sa.actor_id = a.id")
                where_clauses.append("LOWER(a.name) = %s")
                params.append(actor.lower())
            if min_seasons is not None:
                where_clauses.append("s.seasons >= %s")
                params.append(min_seasons)
            if max_seasons is not None:
                where_clauses.append("s.seasons <= %s")
                params.append(max_seasons)
            query += " ".join(joins) + " WHERE " + " AND ".join(where_clauses) if joins or where_clauses[1:] else ""
        if content_type == "all":
            query += " UNION "
        if content_type in ["movie", "all"]:
            query += "SELECT m.title, m.release_year, m.rating, NULL as seasons, m.duration FROM movies m "
            joins = []
            where_clauses = ["1=1"]
            if genre:
                joins.append("JOIN movie_genres mg ON m.id = mg.movie_id JOIN genres g ON mg.genre_id = g.id")
                where_clauses.append("LOWER(g.name) = %s")
                params.append(genre)
            if min_rating:
                where_clauses.append("m.rating >= %s")
                params.append(min_rating)
            if year_from:
                where_clauses.append("m.release_year >= %s")
                params.append(year_from)
            if year_to:
                where_clauses.append("m.release_year <= %s")
                params.append(year_to)
            if country:
                where_clauses.append("LOWER(s.country) = %s")
                params.append(country)
            if language:
                where_clauses.append("LOWER(s.language) = %s")
                params.append(language)
            if age_rating:
                where_clauses.append("m.age_rating = %s")
                params.append(age_rating)
            if director:
                joins.append("JOIN directors d ON m.director_id = d.id")
                where_clauses.append("LOWER(d.name) = %s")
                params.append(director)
            if actor:
                joins.append("JOIN movie_actors ma ON m.id = ma.movie_id JOIN actors a ON ma.actor_id = a.id")
                where_clauses.append("LOWER(a.name) = %s")
                params.append(actor.lower())
            query += " ".join(joins) + " WHERE " + " AND ".join(where_clauses) if joins or where_clauses[1:] else ""
        query += ") AS results "
        if sort_by == "rating":
            query += "ORDER BY rating DESC "
        elif sort_by == "year":
            query += "ORDER BY release_year DESC "
        elif sort_by == "seasons":
            query += "ORDER BY seasons DESC "
        query += f"LIMIT {limit}"
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

    def get_actors(self, title, is_movie):
        table = "movies" if is_movie else "series"
        join_table = "movie_actors" if is_movie else "series_actors"
        self.cursor.execute(f"""
            SELECT DISTINCT a.name
            FROM {table} t
            JOIN {join_table} ta ON t.id = ta.{'movie' if is_movie else 'series'}_id
            JOIN actors a ON ta.actor_id = a.id
            WHERE t.title = %s
        """, (title,))
        return [row[0] for row in self.cursor.fetchall()][:3]  # Ограничиваем до 3 актёров

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