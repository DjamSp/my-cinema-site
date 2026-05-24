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

files = {
    'manage.py': """#!/usr/bin/env python
import os
import sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:import os
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
        raise ImportError("Django not found")
    execute_from_command_line(sys.argv)
if __name__ == '__main__':
    main()""",

    'cinema_project/settings.py': """
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'secret-key-123'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','movies',]
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware',]
ROOT_URLCONF = 'cinema_project.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [os.path.join(BASE_DIR, 'templates')],'APP_DIRS': True,'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages',],},},]
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3',}}
LANGUAGE_CODE = 'ru-ru'
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'""",

    'cinema_project/urls.py': "from django.contrib import admin\nfrom django.urls import path, include\nurlpatterns = [path('admin/', admin.site.urls), path('', include('movies.urls'))]",
    
    'movies/models.py': """from django.db import models
class Category(models.Model):
    name = models.CharField("Жанр", max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    def __str__(self): return self.name
class Movie(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    poster = models.URLField("Ссылка на постер")
    year = models.PositiveIntegerField("Год")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.FloatField("Рейтинг", default=0.0)
    def __str__(self): return self.title""",

    'movies/urls.py': "from django.urls import path\nfrom . import views\nurlpatterns = [path('', views.movie_list, name='home'), path('movie/<int:pk>/', views.movie_detail, name='detail')]",

    'movies/views.py': """from django.shortcuts import render, get_object_or_404
from .models import Movie, Category
def movie_list(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')
    if query: movies = movies.filter(title__icontains=query)
    return render(request, 'movies/index.html', {'movies': movies, 'categories': categories})
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/detail.html', {'movie': movie})""",

    'templates/base.html': """<!DOCTYPE html><html lang="ru"><head><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>body{background:#0f0f0f;color:#fff}.navbar{background:#1a1a1a;border-bottom:2px solid red}</style></head><body><nav class="navbar navbar-dark mb-4"><div class="container"><a class="navbar-brand text-danger fw-bold" href="/">КИНОПАРК</a><form class="d-flex" action="/" method="get"><input class="form-control me-2 bg-dark text-white" type="search" name="q" placeholder="Поиск..."><button class="btn btn-outline-danger" type="submit">Найти</button></form></div></nav><div class="container">{% block content %}{% endblock %}</div></body></html>""",

    'templates/movies/index.html': """{% extends 'base.html' %}{% block content %}<div class="row">{% for m in movies %}<div class="col-md-4 mb-4"><div class="card bg-dark text-white"><img src="{{m.poster}}" class="card-img-top" style="height:300px;object-fit:cover"><div class="card-body"><h5>{{m.title}}</h5><p class="text-warning">{{m.rating}}</p><a href="{% url 'detail' m.id %}" class="btn btn-danger btn-sm">Смотреть</a></div></div></div>{% endfor %}</div>{% endblock %}""",
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Проект успешно создан! Теперь выполни: python manage.py migrate")