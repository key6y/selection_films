import psycopg2
from main import ExpertSystem
import sys
import os

# Установка кодировки UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Динамическая конфигурация подключения к базе данных
is_docker = os.environ.get('DOCKER_ENV', 'false').lower() == 'true'
# Принудительно используем "db" внутри контейнера, если запущены через docker exec
db_config = {
    "host": "db" if is_docker or 'DOCKER_ENV' in os.environ else "localhost",
    "database": "movie_recommendation_system",
    "user": "postgres",
    "password": "luntik2406",
    "port": "5432",
    "options": "-c client_encoding=UTF8"
}

def get_db_connection():
    return psycopg2.connect(**db_config)

def main():
    try:
        with get_db_connection() as conn:
            expert_system = ExpertSystem(conn)
            while True:
                print("\n🎬 === Экспертная система подбора фильмов и сериалов === 🎬")
                print("Главное меню:")
                print("1. 🎥 Получить рекомендации")
                print("2. 📋 Просмотреть доступные варианты")
                print("3. 🚪 Выход")
                choice = input("Выберите действие: ")

                if choice == "1":
                    print("\n=== Параметры поиска ===")
                    content_type = input("Тип контента (Фильм/Сериал/Все): ").lower()
                    while content_type not in ["фильм", "сериал", "все"]:
                        content_type = input("Некорректный ввод. Допустимые значения: Фильм, Сериал, Все: ").lower()

                    genre = input("Жанр (оставьте пустым для любого, примеры: Драма, Комедия, Фантастика, Триллер, Боевик): ").lower()
                    valid_genres = ["драма", "комедия", "фантастика", "триллер", "боевик"]
                    while genre and genre not in valid_genres:
                        print(f"Некорректный жанр '{genre}'. Допустимые значения: {', '.join(valid_genres)}")
                        genre = input("Введите жанр заново: ").lower()

                    min_rating = float(input("Минимальный рейтинг (0-10): ") or 0)
                    while min_rating < 0 or min_rating > 10:
                        min_rating = float(input("Некорректный ввод. Введите рейтинг от 0 до 10: ") or 0)

                    year_from = int(input("Год выпуска от: ") or 1900)
                    year_to = int(input("Год выпуска до: ") or 2025)
                    while year_from > year_to:
                        print("Год начала не может быть больше года окончания!")
                        year_from = int(input("Год выпуска от: ") or 1900)
                        year_to = int(input("Год выпуска до: ") or 2025)

                    country = input("Страна (оставьте пустым для любой): ").lower() or None
                    language = input("Язык (оставьте пустым для любого): ").lower() or None
                    age_rating = input("Возрастной рейтинг (оставьте пустым для любого): ") or None
                    director = input("Режиссер (оставьте пустым для любого): ") or None
                    actor = input("Актёр (оставьте пустым для любого): ") or None

                    min_seasons = None
                    max_seasons = None
                    if content_type in ["сериал", "все"]:
                        min_seasons = int(input("Минимальное количество сезонов (оставьте пустым для любого): ") or 0)
                        max_seasons = int(input("Максимальное количество сезонов (оставьте пустым для любого): ") or 999)

                    limit = int(input("Количество результатов (по умолчанию 10): ") or 10)
                    while limit <= 0:
                        limit = int(input("Некорректный ввод. Введите положительное число: ") or 10)

                    print("\nСортировать по:")
                    print("1. По рейтингу")
                    print("2. По году выпуска")
                    print("3. По количеству сезонов")
                    sort_by = input("Выберите вариант (1-3): ")
                    while sort_by not in ["1", "2", "3"]:
                        sort_by = input("Некорректный ввод. Выберите вариант (1-3): ")
                    sort_by = {"1": "rating", "2": "year", "3": "seasons"}[sort_by]

                    recommendations = expert_system.get_recommendations(
                        content_type={"фильм": "movie", "сериал": "series", "все": "all"}[content_type],
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
                    print("\n=== Поиск рекомендаций ===")
                    if recommendations:
                        print("=== Результаты поиска ===")
                        for i, (title, year, rating, seasons, duration) in enumerate(recommendations, 1):
                            content_type_display = "Фильм" if duration else "Сериал"
                            print(f"{i}. {title} ({year}), Рейтинг: {rating}, {duration or f'{seasons} сезонов'}")
                            genres = expert_system.get_genres(title, duration is not None)
                            if genres:
                                print(f"   Жанры: {', '.join(genres)}")
                            director = expert_system.get_director(title, duration is not None)
                            if director:
                                print(f"   Режиссер: {director}")
                            print(f"   Страна: {expert_system.get_country(title, duration is not None)}, Язык: {expert_system.get_language(title, duration is not None)}, Возраст: {expert_system.get_age_rating(title, duration is not None)}")
                    else:
                        print("По вашему запросу ничего не найдено. 😞")
                elif choice == "2":
                    expert_system.view_available_options()
                elif choice == "3":
                    print("До свидания!")
                    break
                else:
                    print("Некорректный выбор. Попробуйте снова.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()