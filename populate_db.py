import os
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
django.setup()

from movies.models import Movie, Category

def populate():
    # Создаем жанры
    sci_fi, _ = Category.objects.get_or_create(name="Фантастика", slug="sci-fi")
    drama, _ = Category.objects.get_or_create(name="Драма", slug="drama")
    action, _ = Category.objects.get_or_create(name="Боевик", slug="action")
    thriller, _ = Category.objects.get_or_create(name="Триллер", slug="thriller")

    # Добавляем фильмы
    movies_data = [
        {
            "title": "Интерстеллар",
            "description": "Эпическое путешествие группы исследователей через черную дыру в поисках нового дома для человечества.",
            "poster": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
            "year": 2014,
            "category": sci_fi,
            "rating": 8.6
        },
        {
            "title": "Начало",
            "description": "Вор, способный проникать в чужие сны, получает задание внедрить идею в подсознание наследника крупной корпорации.",
            "poster": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
            "year": 2010,
            "category": sci_fi,
            "rating": 8.8
        },
        {
            "title": "Тёмный рыцарь",
            "description": "Бэтмен противостоит своему самому опасному противнику - Джокеру, который сеет хаос в Готэме.",
            "poster": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg",
            "year": 2008,
            "category": action,
            "rating": 9.0
        },
        {
            "title": "Побег из Шоушенка",
            "description": "Банкир, осужденный за убийство жены, организует побег из тюрьмы, где провел 20 лет.",
            "poster": "https://m.media-amazon.com/images/M/MV5BMDA2NDcwMjMtODQ1Yy00YTBjLTg0MjYtMjhiYThhYzE2ZGNiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
            "year": 1994,
            "category": drama,
            "rating": 9.3
        }
    ]

    for movie_data in movies_data:
        obj, created = Movie.objects.get_or_create(
            title=movie_data["title"],
            defaults=movie_data
        )
        if created:
            print(f"Добавлен фильм: {obj.title}")

    print("\nБаза данных успешно наполнена!")

if __name__ == '__main__':
    populate()
