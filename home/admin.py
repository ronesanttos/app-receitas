from django.contrib import admin
from home import models


class IngredientInline(admin.TabularInline):
    model = models.Ingredient
    extra = 1

class InstructionInline(admin.TabularInline):
    model = models.Instruction
    extra = 1
    
@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, InstructionInline]
    list_display = 'id', 'name',
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) 

# Register your models here.
