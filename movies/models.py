from django.db import models

class Actor(models.Model):
    name = models.CharField("Имя", max_length=150)
    photo = models.URLField("Фото (ссылка)")
    bio = models.TextField("Биография", blank=True)

    def __str__(self): return self.name

class Movie(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    poster = models.URLField("Постер (ссылка)")
    backdrop = models.URLField("Фон (широкое фото)", blank=True) # Для Hero-баннера
    year = models.PositiveIntegerField("Год")
    rating = models.FloatField("Рейтинг", default=0.0)
    director = models.CharField("Director", max_length=200, blank=True, null=True)
    actors = models.ManyToManyField(Actor, related_name="movies", verbose_name="Актёры")
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    def __str__(self): return self.title
class Category(models.Model):
    name = models.CharField("Жанр", max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    



class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField("About me", blank=True, max_length=500)
    avatar = models.URLField("Avatar URL", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class MovieRating(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField("Rating", choices=[(i, i) for i in range(1, 11)])
    review = models.TextField("Review", blank=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'movie']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.rating}/10"

class Collection(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='collections')
    name = models.CharField("Collection name", max_length=100)
    description = models.TextField("Description", blank=True, max_length=300)
    movies = models.ManyToManyField(Movie, related_name='collections', blank=True)
    is_favorite = models.BooleanField("Favorite collection", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_favorite', 'name']
    
    def __str__(self):
        return f"{self.user.username}: {self.name} ({self.movies.count()} movies)"
