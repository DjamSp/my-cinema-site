import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
django.setup()

from movies.models import Movie, Category, Actor

def run():
    # 1. Создаем категории
    sci_fi, _ = Category.objects.get_or_create(name="Фантастика", slug="sci-fi")
    drama, _ = Category.objects.get_or_create(name="Драма", slug="drama")
    action, _ = Category.objects.get_or_create(name="Боевик", slug="action")

    # 2. Создаем актёров
    leo, _ = Actor.objects.get_or_create(
        name="Леонардо Ди Каприо", 
        photo="https://image.tmdb.org/t/p/w500/wo2hJv0CDvU8IwSTubXvjY1jReady.jpg"
    )
    cillian, _ = Actor.objects.get_or_create(
        name="Киллиан Мёрфи", 
        photo="https://image.tmdb.org/t/p/w500/llmZ766X9Y6S778n989Y09f5Y97.jpg"
    )
    mcconaughey, _ = Actor.objects.get_or_create(
        name="Мэттью Макконахи", 
        photo="https://image.tmdb.org/t/p/w500/e9p9t97v69oBv9Y89998099898.jpg"
    )

    # 3. Добавляем фильмы и связываем с актёрами
    # Интерстеллар
    m1, _ = Movie.objects.get_or_create(
        title="Интерстеллар",
        defaults={
            'description': "Когда человечество стоит на грани вымирания, группа исследователей отправляется в самую важную миссию в истории: путешествие за пределы нашей галактики.",
            'poster': "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6vCU6mG2vI3LB.jpg",
            'year': 2014,
            'rating': 8.7,
            'category': sci_fi,
            
        }
    )
    m1.actors.add(mcconaughey)

    # Оппенгеймер
    m2, _ = Movie.objects.get_or_create(
        title="Оппенгеймер",
        defaults={
            'description': "История жизни американского физика Роберта Оппенгеймера, который стоял во главе первых разработок ядерного оружия.",
            'poster': "https://image.tmdb.org/t/p/w500/8GxvA9zDZ96eS3yvS9Xhno8S8S.jpg",
            'year': 2023,
            'rating': 8.4,
            'category': drama,
            
        }
    )
    m2.actors.add(cillian)

    # Начало
    m3, _ = Movie.objects.get_or_create(
        title="Начало",
        defaults={
            'description': "Кобб — талантливый вор, лучший в искусстве извлечения ценных секретов из глубин подсознания во время сна.",
            'poster': "https://image.tmdb.org/t/p/w500/edv5CZvRjSME5zX0STCcIPStvS0.jpg",
            'year': 2010,
            'rating': 8.8,
            'category': sci_fi,
            
        }
    )
    m3.actors.add(leo)

    print("Данные успешно загружены! Актёры привязаны к фильмам.")

if __name__ == '__main__':
    run()
