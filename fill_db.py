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

    # Добавляем фильмы
    Movie.objects.get_or_create(
        title="Интерстеллар",
        description="Эпическое путешествие через черную дыру.",
        poster="https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
        year=2014,
        category=sci_fi,
        rating=8.6
    )

    Movie.objects.get_or_create(
        title="Начало",
        description="Проникновение в чужие сны.",
        poster="https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
        year=2010,
        category=sci_fi,
        rating=8.8
    )

    print("База данных успешно наполнена!")

if __name__ == '__main__':
    populate()