from flask import Flask, render_template, request, jsonify
import psycopg2
import sys

# Установка кодировки UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Конфигурация подключения к базе данных
db_config = {
    "host": "localhost",
    "database": "movie_recommendation_system",
    "user": "postgres",
    "password": "luntik2406",
    "port": "5432",
    "options": "-c client_encoding=UTF8"
}

def get_db_connection():
    return psycopg2.connect(**db_config)

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

    def get_available_options(self):
        self.cursor.execute("SELECT name FROM genres")
        genres = [row[0] for row in self.cursor.fetchall()]
        self.cursor.execute("SELECT name FROM actors")
        actors = [row[0] for row in self.cursor.fetchall()]
        self.cursor.execute("SELECT name FROM directors")
        directors = [row[0] for row in self.cursor.fetchall()]
        return {"genres": genres, "actors": actors, "directors": directors}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        with get_db_connection() as conn:
            expert_system = ExpertSystem(conn)
            data = request.form
            content_type = data.get('content_type', 'all')
            genre = data.get('genre') or None
            min_rating = float(data.get('min_rating') or 0)
            year_from = int(data.get('year_from') or 1900)
            year_to = int(data.get('year_to') or 2025)
            country = data.get('country') or None
            language = data.get('language') or None
            age_rating = data.get('age_rating') or None
            director = data.get('director') or None
            actor = data.get('actor') or None
            min_seasons = int(data.get('min_seasons') or 0) if content_type in ["series", "all"] else None
            max_seasons = int(data.get('max_seasons') or 999) if content_type in ["series", "all"] else None
            limit = int(data.get('limit') or 10)
            sort_by = data.get('sort_by', 'rating')

            recommendations = expert_system.get_recommendations(
                content_type=content_type,
                genre=genre,
                min_rating=min_rating,
                year_from=year_from,
                year_to=year_to,
                country=country,
                language=language,
                age_rating=age_rating,
                director=director,
                actor=actor,
                min_seasons=min_seasons,
                max_seasons=max_seasons,
                sort_by=sort_by,
                limit=limit
            )

            results = []
            for title, year, rating, seasons, duration in recommendations:
                is_movie = duration is not None
                genres = expert_system.get_genres(title, is_movie)
                director = expert_system.get_director(title, is_movie)
                country = expert_system.get_country(title, is_movie)
                language = expert_system.get_language(title, is_movie)
                age_rating = expert_system.get_age_rating(title, is_movie)
                results.append({
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "duration": duration if is_movie else f"{seasons} сезонов",
                    "type": "Фильм" if is_movie else "Сериал",
                    "genres": genres,
                    "director": director,
                    "country": country,
                    "language": language,
                    "age_rating": age_rating
                })
            return jsonify({"recommendations": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/options', methods=['GET'])
def get_options():
    try:
        with get_db_connection() as conn:
            expert_system = ExpertSystem(conn)
            options = expert_system.get_available_options()
            return jsonify(options)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)