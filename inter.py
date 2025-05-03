from main import MovieExpertSystem
from colorama import init, Fore, Style
import time
import sys
import os

# Инициализация colorama для цветного текста
init(autoreset=True)

class MovieRecommendationInterface:
    def __init__(self, db_config):
        """Инициализация интерфейса"""
        self.expert_system = MovieExpertSystem(db_config)
    
    def start(self):
        """Запуск интерфейса"""
        print(Fore.CYAN + "\n🎬 === Экспертная система подбора фильмов и сериалов === 🎬")
        
        while True:
            print(Fore.YELLOW + "\nГлавное меню:")
            print("1. 🎥 Получить рекомендации")
            print("2. 📋 Просмотреть доступные варианты")
            print("3. 🚪 Выход")
            
            choice = input(Fore.GREEN + "Выберите действие: ").strip()
            
            if choice == '1':
                self._get_recommendations()
            elif choice == '2':
                self._show_options()
            elif choice == '3':
                print(Fore.RED + "До свидания! 👋")
                self.expert_system.close()
                break
            else:
                print(Fore.RED + "Некорректный ввод. Пожалуйста, выберите 1, 2 или 3. ⚠️")
    
    def _get_recommendations(self):
        """Получение рекомендаций"""
        print(Fore.CYAN + "\n=== Параметры поиска ===")
        
        # Опции для сортировки
        sort_options = {'1': 'rating', '2': 'year', '3': 'seasons'}
        
        preferences = {
            'type': self._get_input("Тип контента (movie/series/all): ", ['movie', 'series', 'all'], 'all'),
            'genre': self._get_input("Жанр (оставьте пустым для любого): ", 
                                    self.expert_system.get_available_options('genres'), ''),
            'min_rating': self._get_float_input("Минимальный рейтинг (0-10): ", 0, 10),
            'year_from': self._get_int_input("Год выпуска от: "),
            'year_to': self._get_int_input("Год выпуска до: "),
            'country': self._get_input("Страна (оставьте пустым для любой): ",
                                     self.expert_system.get_available_options('countries'), ''),
            'language': self._get_input("Язык (оставьте пустым для любого): ",
                                       self.expert_system.get_available_options('languages'), ''),
            'age_rating': self._get_input("Возрастной рейтинг (оставьте пустым для любого): ",
                                         self.expert_system.get_available_options('age_ratings'), ''),
            'director': self._get_input("Режиссер (оставьте пустым для любого): ",
                                       self.expert_system.get_available_options('directors'), ''),
            'actor': self._get_input("Актер (оставьте пустым для любого): ",
                                    self.expert_system.get_available_options('actors'), ''),
            'min_seasons': self._get_int_input("Минимальное количество сезонов (для сериалов, оставьте пустым для любого): ", 1, 50, None),
            'max_seasons': self._get_int_input("Максимальное количество сезонов (для сериалов, оставьте пустым для любого): ", 1, 50, None),
            'limit': self._get_int_input("Количество результатов (по умолчанию 10): ", 1, 100, 10)
        }
        
        # Запрос сортировки
        print(Fore.YELLOW + "\nСортировать по:")
        print("1. По рейтингу")
        print("2. По году выпуска")
        print("3. По количеству сезонов")
        sort_choice = self._get_input("Выберите вариант (1-3): ", ['1', '2', '3'], '1')
        preferences['sort_by'] = sort_options[sort_choice]
        
        # Удаляем пустые параметры
        preferences = {k: v for k, v in preferences.items() if v not in [None, '']}
        
        print(Fore.CYAN + "\n=== Поиск рекомендаций ===")
        self._loading_animation()
        
        recommendations = self.expert_system.recommend(preferences)
        
        if not recommendations:
            print(Fore.RED + "По вашему запросу ничего не найдено. 😞")
            return
        
        print(Fore.CYAN + "\n=== Результаты поиска ===")
        for i, item in enumerate(recommendations, 1):
            print(Fore.GREEN + f"{i}. {item['details']}")
            print(Fore.BLUE + f"   Жанры: {item['genres']}")
            print(Fore.BLUE + f"   Режиссер: {item['director'] or 'Не указан'}")
            print(Fore.BLUE + f"   Страна: {item['country']}, Язык: {item['language']}, Возраст: {item['age_rating']}\n")
    
    def _show_options(self):
        """Просмотр доступных вариантов"""
        print(Fore.YELLOW + "\nДоступные категории для просмотра:")
        categories = {
            'genres': 'Жанры',
            'countries': 'Страны',
            'languages': 'Языки',
            'age_ratings': 'Возрастные рейтинги',
            'directors': 'Режиссеры',
            'actors': 'Актеры'
        }
        
        name_to_key = {value.lower(): key for key, value in categories.items()}
        
        for key, value in categories.items():
            print(Fore.BLUE + f"📌 {value}")
        
        choice = input(Fore.GREEN + "\nВыберите категорию (или нажмите Enter для возврата): ").strip()
        
        if not choice:
            print(Fore.YELLOW + "Возврат в главное меню. 🔙")
            return
        
        choice_lower = choice.lower()
        if choice_lower in name_to_key:
            category_key = name_to_key[choice_lower]
            options = self.expert_system.get_available_options(category_key)
            print(Fore.CYAN + f"\n{categories[category_key]}:")
            if not options:
                print(Fore.RED + "Нет доступных опций для этой категории. 🚫")
            else:
                for i, option in enumerate(options, 1):
                    print(Fore.BLUE + f"{i}. {option}")
        else:
            print(Fore.RED + "Некорректная категория. Попробуйте снова. ⚠️")
    
    def _get_input(self, prompt, options=None, default=None):
        """Получение ввода с валидацией"""
        while True:
            value = input(Fore.GREEN + prompt).strip()
            if not value and default is not None:
                return default
            if options is None or not options or value in options:
                return value if value else None
            print(Fore.RED + f"Некорректный ввод. Допустимые значения: {', '.join(options)}")
    
    def _get_int_input(self, prompt, min_val=None, max_val=None, default=None):
        """Получение целочисленного ввода"""
        while True:
            value = input(Fore.GREEN + prompt).strip()
            if not value and default is not None:
                return default
            try:
                num = int(value)
                if (min_val is None or num >= min_val) and (max_val is None or num <= max_val):
                    return num
                print(Fore.RED + f"Число должно быть между {min_val} и {max_val}.")
            except ValueError:
                print(Fore.RED + "Пожалуйста, введите целое число (например, 5).")
    
    def _get_float_input(self, prompt, min_val=None, max_val=None, default=None):
        """Получение дробного ввода"""
        while True:
            value = input(Fore.GREEN + prompt).strip()
            if not value and default is not None:
                return default
            try:
                num = float(value)
                if (min_val is None or num >= min_val) and (max_val is None or num <= max_val):
                    return num
                print(Fore.RED + f"Число должно быть между {min_val} и {max_val}.")
            except ValueError:
                print(Fore.RED + "Пожалуйста, введите число (например, 7.5).")
    
    def _loading_animation(self):
        """Анимация загрузки"""
        animation = "|/-\\"
        for _ in range(10):
            sys.stdout.write(Fore.YELLOW + f"\rПоиск... {animation[_ % 4]}")
            sys.stdout.flush()
            time.sleep(0.2)
        print("\r" + " " * 20 + "\r", end="")

if __name__ == "__main__":
    # Получение параметров подключения из переменных окружения
    db_config = {
        'dbname': os.getenv('DB_NAME', 'movie_recommendation_system'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'luntik2406'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    interface = MovieRecommendationInterface(db_config)
    interface.start()