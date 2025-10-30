from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage #type:ignore

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
class Recipe(models.Model):
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    preparation_time = models.PositiveIntegerField(blank=True, null=True)
    cooking_time = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='recipes/', storage=MediaCloudinaryStorage())
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
        
    )
    @property
    def total_time(self):
        return (self.preparation_time or 0) + (self.cooking_time or 0) 
    
    def __str__(self) -> str:
        return f'{self.name}'

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instruction')
    step = models.CharField()
    ordem = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['ordem']
        
    def __str__(self):
        return f'Passo {self.ordem}'

  
class Favorite(models.Model):
    session_key  = models.CharField( max_length=40, db_index=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('session_key', 'recipe')
        
    def __str__(self):
        return f'{self.session_key } -> {self.recipe.name}'
