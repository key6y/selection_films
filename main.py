from db import Database

class MovieExpertSystem:
    def __init__(self, db_config):
        """Инициализация экспертной системы"""
        self.db = Database(**db_config)
    
    def recommend(self, preferences):
        """Основной метод рекомендации"""
        content_type = preferences.get('type', 'all')
        limit = preferences.pop('limit', 10) if 'limit' in preferences else 10
        sort_by = preferences.pop('sort_by', 'rating') if 'sort_by' in preferences else 'rating'
        
        results = []
        if content_type in ['movie', 'all']:
            movies = self.db.get_movies({**preferences, 'type': 'movie', 'limit': limit})
            if movies:
                results.extend([{'type': 'movie', **self._format_movie(m)} for m in movies])
        
        if content_type in ['series', 'all']:
            series = self.db.get_series({**preferences, 'type': 'series', 'limit': limit})
            if series:
                results.extend([{'type': 'series', **self._format_series(s)} for s in series])
        
        # Сортировка результатов
        if sort_by == 'year':
            return sorted(results, key=lambda x: x['year'], reverse=True)[:limit]
        elif sort_by == 'seasons':
            return sorted(results, key=lambda x: x.get('seasons', 0), reverse=True)[:limit]
        else:  # по умолчанию сортировка по рейтингу
            return sorted(results, key=lambda x: x['rating'], reverse=True)[:limit]
    
    def get_available_options(self, field):
        """Получение доступных вариантов для полей"""
        result = self.db.get_options(field)
        if isinstance(result, bool):
            return []
        return [item[0] for item in result]
    
    def _format_movie(self, movie_data):
        """Форматирование данных о фильме"""
        return {
            'id': movie_data[0],
            'title': movie_data[1],
            'year': movie_data[2],
            'rating': float(movie_data[3]) if movie_data[3] else None,
            'duration': movie_data[4],
            'director': movie_data[5],
            'country': movie_data[6],
            'language': movie_data[7],
            'age_rating': movie_data[8],
            'genres': movie_data[9],
            'details': f"{movie_data[1]} ({movie_data[2]}), Рейтинг: {movie_data[3]}, {movie_data[4]} мин"
        }
    
    def _format_series(self, series_data):
        """Форматирование данных о сериале"""
        return {
            'id': series_data[0],
            'title': series_data[1],
            'year': series_data[2],
            'rating': float(series_data[3]) if series_data[3] else None,
            'seasons': series_data[4],
            'director': series_data[5],
            'country': series_data[6],
            'language': series_data[7],
            'age_rating': series_data[8],
            'genres': series_data[9],
            'details': f"{series_data[1]} ({series_data[2]}), Рейтинг: {series_data[3]}, {series_data[4]} сезонов"
        }
    
    def close(self):
        """Закрытие соединения с базой данных"""
        self.db.close()