from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('perfil', views.perfil, name='perfil'),
    
    path('favoritos', views.favorites, name='favorites'),
    path('favoritos/<int:recipe_id>/', views.toggle_favorites, name='toggle_favorites'),
    
    #recipe
    path('recipe/<int:recipe_id>/', views.recipe_id, name='recipe_id'),
    path('recipe/create/', views.create, name='create'),
    path('recipe/<int:recipe_id>/update/', views.update_recipe, name='update'),
    path('recipe/<int:recipe_id>/delete/', views.delete, name='delete'),
    
    #user
    path('user/register', views.register, name='register'),
    path('user/login', views.login, name='login'),
    path('user/logout', views.logout, name='logout'),
    path('user/update', views.update, name='update'),
]
