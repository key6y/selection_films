from flask import Flask, render_template, request, jsonify
import psycopg2
import sys
from main import ExpertSystem  # Импортируем ExpertSystem из main.py

# Установка кодировки UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Конфигурация подключения к базе данных (для Docker)
db_config = {
    "host": "db",
    "database": "movie_recommendation_system",
    "user": "postgres",
    "password": "luntik2406",
    "port": "5432",
    "options": "-c client_encoding=UTF8"
}

def get_db_connection():
    return psycopg2.connect(**db_config)

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
                actors = expert_system.get_actors(title, is_movie)  # Добавляем актёров
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
                    "actors": actors,  # Добавляем в результат
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