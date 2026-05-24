import os

# Структура проекта
folders = [
    'cinema_project',
    'movies',
    'movies/migrations',
    'templates',
    'templates/movies',
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Создаем manage.py
with open('manage.py', 'w', encoding='utf-8') as f:
    f.write("""#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""")

# Создаем settings.py
with open('cinema_project/settings.py', 'w', encoding='utf-8') as f:
    f.write("""from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'secret-key-123'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cinema_project.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""")

# Создаем urls.py
with open('cinema_project/urls.py', 'w', encoding='utf-8') as f:
    f.write("""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
]
""")

# Создаем models.py
with open('movies/models.py', 'w', encoding='utf-8') as f:
    f.write("""from django.db import models

class Category(models.Model):
    name = models.CharField("Жанр", max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Movie(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    poster = models.URLField("Ссылка на постер")
    year = models.PositiveIntegerField("Год")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Жанр")
    rating = models.FloatField("Рейтинг", default=0.0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
""")

# Создаем urls.py для movies
with open('movies/urls.py', 'w', encoding='utf-8') as f:
    f.write("""from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='home'),
    path('movie/<int:pk>/', views.movie_detail, name='detail'),
]
""")

# Создаем views.py
with open('movies/views.py', 'w', encoding='utf-8') as f:
    f.write("""from django.shortcuts import render, get_object_or_404
from .models import Movie, Category

def movie_list(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')
    if query:
        movies = movies.filter(title__icontains=query)
    return render(request, 'movies/index.html', {'movies': movies, 'categories': categories})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/detail.html', {'movie': movie})
""")

# Создаем base.html
with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: #0f0f0f;
            color: #fff;
        }
        .navbar {
            background: #1a1a1a;
            border-bottom: 2px solid red;
        }
        .card {
            transition: transform 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
    </style>
    <title>Кинопарк</title>
</head>
<body>
    <nav class="navbar navbar-dark mb-4">
        <div class="container">
            <a class="navbar-brand text-danger fw-bold fs-3" href="/"> КИНОПАРК</a>
            <form class="d-flex" action="/" method="get">
                <input class="form-control me-2 bg-dark text-white" type="search" name="q" placeholder="Поиск фильмов..." style="width: 300px;">
                <button class="btn btn-outline-danger" type="submit">Найти</button>
            </form>
        </div>
    </nav>
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
""")

# Создаем index.html
with open('templates/movies/index.html', 'w', encoding='utf-8') as f:
    f.write("""{% extends 'base.html' %}

{% block content %}
<h1 class="mb-4 text-danger"> Популярные фильмы</h1>
<div class="row">
    {% for movie in movies %}
    <div class="col-md-4 mb-4">
        <div class="card bg-dark text-white h-100">
            <img src="{{ movie.poster }}" class="card-img-top" style="height: 400px; object-fit: cover;" alt="{{ movie.title }}">
            <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text text-muted">{{ movie.year }} • {{ movie.category.name }}</p>
                <div class="text-warning mb-2">
                    ★ {{ movie.rating }}
                </div>
                <a href="{% url 'detail' movie.id %}" class="btn btn-danger">Подробнее</a>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12">
        <p class="text-center">Фильмы не найдены</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
""")

# Создаем detail.html
with open('templates/movies/detail.html', 'w', encoding='utf-8') as f:
    f.write("""{% extends 'base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-4">
        <img src="{{ movie.poster }}" class="img-fluid rounded" alt="{{ movie.title }}">
    </div>
    <div class="col-md-8">
        <h1 class="text-danger">{{ movie.title }}</h1>
        <p class="text-muted">{{ movie.year }} • {{ movie.category.name }}</p>
        <div class="text-warning fs-4 mb-3">
            ★ {{ movie.rating }}
        </div>
        <h4>Описание:</h4>
        <p>{{ movie.description }}</p>
        <a href="{% url 'home' %}" class="btn btn-outline-danger mt-3">← Назад к фильмам</a>
    </div>
</div>
{% endblock %}
""")

# Создаем скрипт для наполнения БД
with open('populate_db.py', 'w', encoding='utf-8') as f:
    f.write("""import os
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

    print("\\nБаза данных успешно наполнена!")

if __name__ == '__main__':
    populate()
""")

print(" Проект создан!")
print("\n команды:")
print("1. python manage.py makemigrations")
print("2. python manage.py migrate")
print("3. python populate_db.py")
print("4. python manage.py runserver")