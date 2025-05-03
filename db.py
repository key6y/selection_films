import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, dbname, user, password, host, port):
        """Инициализация соединения с базой данных"""
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise
    
    def get_movies(self, filters):
        """Получение фильмов с фильтрацией"""
        query = sql.SQL("""
            SELECT m.id, m.title, m.release_year, m.rating, m.duration, 
                   d.name as director, m.country, m.language, m.age_rating,
                   STRING_AGG(g.name, ', ') as genres
            FROM movies m
            LEFT JOIN directors d ON m.director_id = d.id
            LEFT JOIN movie_genres mg ON m.id = mg.movie_id
            LEFT JOIN genres g ON mg.genre_id = g.id
            {where}
            GROUP BY m.id, d.name
            ORDER BY m.rating DESC
            {limit}
        """).format(
            where=self._build_where_clause(filters),
            limit=sql.SQL("LIMIT %s") if filters.get('limit') else sql.SQL("")
        )
        
        params = [p for p in [
            filters.get('genre'),
            filters.get('min_rating'),
            filters.get('year_from'),
            filters.get('year_to'),
            filters.get('country'),
            filters.get('language'),
            filters.get('age_rating'),
            filters.get('director'),
            filters.get('actor'),
            filters.get('limit')
        ] if p is not None]
        
        return self.execute_query(query, params)
    
    def get_series(self, filters):
        """Получение сериалов с фильтрацией"""
        query = sql.SQL("""
            SELECT s.id, s.title, s.release_year, s.rating, s.seasons, 
                   d.name as director, s.country, s.language, s.age_rating,
                   STRING_AGG(g.name, ', ') as genres
            FROM series s
            LEFT JOIN directors d ON s.director_id = d.id
            LEFT JOIN series_genres sg ON s.id = sg.series_id
            LEFT JOIN genres g ON sg.genre_id = g.id
            {where}
            GROUP BY s.id, d.name
            ORDER BY s.rating DESC
            {limit}
        """).format(
            where=self._build_where_clause(filters),
            limit=sql.SQL("LIMIT %s") if filters.get('limit') else sql.SQL("")
        )
        
        params = [p for p in [
            filters.get('genre'),
            filters.get('min_rating'),
            filters.get('year_from'),
            filters.get('year_to'),
            filters.get('country'),
            filters.get('language'),
            filters.get('age_rating'),
            filters.get('director'),
            filters.get('actor'),
            filters.get('min_seasons'),
            filters.get('max_seasons'),
            filters.get('limit')
        ] if p is not None]
        
        return self.execute_query(query, params)
    
    def get_options(self, field):
        """Получение доступных вариантов для полей"""
        queries = {
            'genres': "SELECT name FROM genres ORDER BY name",
            'countries': """
                (SELECT DISTINCT country FROM movies)
                UNION
                (SELECT DISTINCT country FROM series)
                ORDER BY country
            """,
            'languages': """
                (SELECT DISTINCT language FROM movies)
                UNION
                (SELECT DISTINCT language FROM series)
                ORDER BY language
            """,
            'age_ratings': """
                (SELECT DISTINCT age_rating FROM movies)
                UNION
                (SELECT DISTINCT age_rating FROM series)
                ORDER BY age_rating
            """,
            'directors': "SELECT name FROM directors ORDER BY name",
            'actors': "SELECT name FROM actors ORDER BY name"
        }
        return self.execute_query(queries.get(field, "SELECT NULL LIMIT 0"))
    
    def execute_query(self, query, params=None, fetch=True):
        """Выполнение SQL-запроса"""
        try:
            if isinstance(query, sql.Composed):
                query_str = query.as_string(self.cursor)
            else:
                query_str = query
            self.cursor.execute(query, params or ())
            if fetch and self.cursor.description:
                result = self.cursor.fetchall()
                return result
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Database error: {e}")
            return False
    
    def _build_where_clause(self, filters):
        """Построение условия WHERE"""
        conditions = []
        params = []
        
        if filters.get('genre'):
            if filters.get('type') == 'movie':
                conditions.append(sql.SQL("m.id IN (SELECT movie_id FROM movie_genres WHERE genre_id IN (SELECT id FROM genres WHERE name = %s))"))
            else:  # series
                conditions.append(sql.SQL("s.id IN (SELECT series_id FROM series_genres WHERE genre_id IN (SELECT id FROM genres WHERE name = %s))"))
            params.append(filters['genre'])
        
        if filters.get('min_rating'):
            conditions.append(sql.SQL("rating >= %s"))
            params.append(filters['min_rating'])
        
        if filters.get('year_from'):
            conditions.append(sql.SQL("release_year >= %s"))
            params.append(filters['year_from'])
        
        if filters.get('year_to'):
            conditions.append(sql.SQL("release_year <= %s"))
            params.append(filters['year_to'])
        
        if filters.get('country'):
            conditions.append(sql.SQL("country = %s"))
            params.append(filters['country'])
        
        if filters.get('language'):
            conditions.append(sql.SQL("language = %s"))
            params.append(filters['language'])
        
        if filters.get('age_rating'):
            conditions.append(sql.SQL("age_rating = %s"))
            params.append(filters['age_rating'])
        
        if filters.get('director'):
            conditions.append(sql.SQL("director_id IN (SELECT id FROM directors WHERE name = %s)"))
            params.append(filters['director'])
        
        if filters.get('actor'):
            if filters.get('type') == 'movie':
                conditions.append(sql.SQL("id IN (SELECT movie_id FROM movie_actors WHERE actor_id IN (SELECT id FROM actors WHERE name = %s))"))
            else:  # series
                conditions.append(sql.SQL("id IN (SELECT series_id FROM series_actors WHERE actor_id IN (SELECT id FROM actors WHERE name = %s))"))
            params.append(filters['actor'])
        
        # Добавляем фильтрацию по сезонам (только для сериалов)
        if filters.get('type') in ['series', 'all']:
            if filters.get('min_seasons'):
                conditions.append(sql.SQL("seasons >= %s"))
                params.append(filters['min_seasons'])
            
            if filters.get('max_seasons'):
                conditions.append(sql.SQL("seasons <= %s"))
                params.append(filters['max_seasons'])
        
        if not conditions:
            return sql.SQL("")
        
        return sql.SQL("WHERE ") + sql.SQL(" AND ").join(conditions)
    
    def close(self):
        """Закрытие соединения"""
        self.cursor.close()
        self.conn.close()