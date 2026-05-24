from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='home'),
    path('movie/<int:pk>/', views.movie_detail, name='detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('rating/<int:movie_id>/', views.add_rating, name='add_rating'),
    path('favorite/<int:movie_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('collection/create/', views.create_collection, name='create_collection'),
    path('collection/<int:collection_id>/', views.collection_detail, name='collection_detail'),
    path('collection/<int:collection_id>/add/<int:movie_id>/', views.add_to_collection, name='add_to_collection'),
    path('collection/<int:collection_id>/delete/', views.delete_collection, name='delete_collection'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('add-movie/', views.add_movie, name='add_movie'),
    path('edit-movie/<int:pk>/', views.edit_movie, name='edit_movie'),
    path('delete-movie/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('actors/', views.actors_list, name='actors'),
    path('categories/', views.categories_list, name='categories'),
    path('directors/', views.directors_list, name='directors'),
]
