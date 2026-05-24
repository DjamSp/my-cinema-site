from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from .models import Movie, Category, Actor, UserProfile, MovieRating, Collection

def is_admin(user):
    return user.is_staff or user.is_superuser

def movie_list(request):
    movies = Movie.objects.select_related('category').prefetch_related('actors', 'ratings').all()
    query = request.GET.get('q')
    
    if query:
        movies = movies.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(director__icontains=query)
        )
    
    for movie in movies:
        movie.avg_rating = movie.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, 'movies/index.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.select_related('category').prefetch_related('actors', 'ratings__user'), pk=pk)
    movie.avg_rating = movie.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    
    user_rating = None
    user_review = None
    if request.user.is_authenticated:
        try:
            user_rating_obj = MovieRating.objects.get(user=request.user, movie=movie)
            user_rating = user_rating_obj.rating
            user_review = user_rating_obj.review
        except MovieRating.DoesNotExist:
            pass
    
    return render(request, 'movies/detail.html', {
        'movie': movie,
        'user_rating': user_rating,
        'user_review': user_review
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'movies/login.html', {'error': 'Invalid credentials'})
    return render(request, 'movies/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        from django.contrib.auth.models import User
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'movies/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'movies/register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        # Автоматически создаем профиль
        UserProfile.objects.get_or_create(user=user)
        
        login(request, user)
        return redirect('profile')
    
    return render(request, 'movies/register.html')

@login_required
def profile(request):
    # Получаем или создаем профиль
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created:
        print(f"Profile created for {request.user.username}")
    
    ratings = MovieRating.objects.filter(user=request.user).select_related('movie')
    collections = Collection.objects.filter(user=request.user).prefetch_related('movies')
    
    favorite_collection, created = Collection.objects.get_or_create(
        user=request.user,
        is_favorite=True,
        defaults={'name': 'Favorites', 'description': 'My favorite movies'}
    )
    
    return render(request, 'movies/profile.html', {
        'profile': profile,
        'ratings': ratings,
        'collections': collections,
        'favorite_collection': favorite_collection
    })

@login_required
def add_rating(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_id)
        rating = request.POST.get('rating')
        review = request.POST.get('review', '')
        
        rating_obj, created = MovieRating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'rating': rating, 'review': review}
        )
        
        return redirect('detail', pk=movie_id)
    
    return redirect('home')

@login_required
def add_to_favorites(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    favorites, _ = Collection.objects.get_or_create(
        user=request.user,
        is_favorite=True,
        defaults={'name': 'Favorites', 'description': 'My favorite movies'}
    )
    
    if movie in favorites.movies.all():
        favorites.movies.remove(movie)
    else:
        favorites.movies.add(movie)
    
    return redirect('detail', pk=movie_id)

@login_required
def create_collection(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        Collection.objects.create(
            user=request.user,
            name=name,
            description=description
        )
        
        return redirect('profile')
    
    return redirect('home')

@login_required
def add_to_collection(request, collection_id, movie_id):
    collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if movie in collection.movies.all():
        collection.movies.remove(movie)
    else:
        collection.movies.add(movie)
    
    return redirect('collection_detail', collection_id=collection_id)

@login_required
def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
    return render(request, 'movies/collection_detail.html', {'collection': collection})

@login_required
def delete_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id, user=request.user)
    if not collection.is_favorite:
        collection.delete()
    return redirect('profile')

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.bio = request.POST.get('bio', '')
        profile.avatar = request.POST.get('avatar', '')
        profile.save()
        return redirect('profile')
    
    return redirect('home')

def actors_list(request):
    actors = Actor.objects.prefetch_related('movies').all()
    return render(request, 'movies/actors.html', {'actors': actors})

def categories_list(request):
    categories = Category.objects.prefetch_related('movie_set').all()
    return render(request, 'movies/categories.html', {'categories': categories})

def directors_list(request):
    directors = Movie.objects.exclude(director__isnull=True).exclude(director__exact='').values_list('director', flat=True).distinct()
    
    directors_data = []
    for director_name in directors:
        movies = Movie.objects.filter(director=director_name)
        directors_data.append({
            'name': director_name,
            'movies_count': movies.count(),
            'movies': movies,
            'rating': sum(m.rating for m in movies) / movies.count() if movies.exists() else 0
        })
    
    return render(request, 'movies/directors.html', {'directors': directors_data})

@user_passes_test(is_admin)
def admin_panel(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    actors = Actor.objects.all()
    return render(request, 'movies/admin_panel.html', {
        'movies': movies,
        'categories': categories,
        'actors': actors
    })

@user_passes_test(is_admin)
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        poster = request.POST.get('poster')
        year = request.POST.get('year')
        rating = request.POST.get('rating')
        director = request.POST.get('director')
        category_id = request.POST.get('category')
        
        movie = Movie.objects.create(
            title=title,
            description=description,
            poster=poster,
            year=year,
            rating=rating,
            director=director,
            category_id=category_id
        )
        
        actor_ids = request.POST.getlist('actors')
        if actor_ids:
            movie.actors.set(actor_ids)
        
        return redirect('admin_panel')
    
    categories = Category.objects.all()
    actors = Actor.objects.all()
    return render(request, 'movies/add_movie.html', {
        'categories': categories,
        'actors': actors
    })

@user_passes_test(is_admin)
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.poster = request.POST.get('poster')
        movie.year = request.POST.get('year')
        movie.rating = request.POST.get('rating')
        movie.director = request.POST.get('director')
        movie.category_id = request.POST.get('category')
        movie.save()
        
        actor_ids = request.POST.getlist('actors')
        movie.actors.set(actor_ids)
        
        return redirect('admin_panel')
    
    categories = Category.objects.all()
    actors = Actor.objects.all()
    return render(request, 'movies/edit_movie.html', {
        'movie': movie,
        'categories': categories,
        'actors': actors
    })

@user_passes_test(is_admin)
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('admin_panel')
