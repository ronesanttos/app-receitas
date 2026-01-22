from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import Paginator
from home.models import Recipe, Favorite
from home.utils import get_user_favorites
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def index(req):
    category_id = req.GET.get('category')
    recipes = Recipe.objects.select_related('category').order_by('-id')
    
    user_favorites = get_user_favorites(req)
    
    if category_id:
        recipes = recipes.filter(category_id=category_id)
        
    paginator = Paginator(recipes,10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        'site_title': 'Receitas',
        'page_obj': page_obj,
        'user_favorites': user_favorites,
        'category_selected': int(category_id) if category_id else None,
    }
    
    return render(req,
        'home/index.html',
        context,)
    
def search(req):
    search_value = req.GET.get('q','').strip()
    category_id = req.GET.get('category')

    user_favorites = get_user_favorites(req)
    
    if search_value == '':
        return redirect('home:index')
    
    recipes = Recipe.objects.select_related('category').filter(
        Q(name__icontains=search_value) |
        Q(description__icontains=search_value) |
        Q(category__name__icontains=search_value)
    ).order_by('-id')

    if category_id:
        recipes = recipes.filter(category_id=category_id)
    
    paginator = Paginator(recipes, 10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title': f'Search - {search_value}',
        'search_value': search_value,
        'user_favorites': user_favorites,
    }
    
    return render(
        req,
        'home/index.html',
        context,
    )
    
def recipe_id(req,recipe_id):
    try:
        single_recipe = Recipe.objects.get(pk=recipe_id)
        user_favorites = get_user_favorites(req)
        
        context = {
            'recipe': single_recipe,
            'site_title': f'{single_recipe.name} - Detalhes',
            'user_favorites': user_favorites,
        }
    
    except Recipe.DoesNotExist:
        return redirect('home:index')
    
    return render(
        req,
        'home/recipe_id.html',
        context,
    )

def favorites(req):
    if not req.session.session_key:
        req.session.create()
        
    session_key = req.session.session_key
    
    favorites = Favorite.objects.filter(session_key=session_key).select_related("recipe")
    
    
    context = {
        'site_title': 'Favoritos',
        'favorites': favorites,
    }
    
    return render(req,"home/favorites.html", context)

def toggle_favorites(req,recipe_id):
    if not req.session.session_key:
        req.session.create()
        
    session_key = req.session.session_key
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    favorite = Favorite.objects.filter(session_key=session_key,recipe=recipe).first()
    
    if favorite:
        favorite.delete()
    
    else:
        Favorite.objects.create(session_key=session_key, recipe=recipe)
        
    # Redireciona de volta à página anterior (ou favoritos)
    return redirect(req.META.get('HTTP_REFERER', 'home:favorites'))

@login_required(login_url='home:login')
def perfil(req):
    recipes = Recipe.objects.filter(owner=req.user).order_by('-id')
    
    paginator = Paginator(recipes, 10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        'site_title': 'Perfil',
        'page_obj': page_obj,
    }
    
    return render(req,
        'home/perfil.html',
        context,)