from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from home.models import Recipe
from home.form import RecipeForm, InstructionFormSet, IngredientFormSet

@login_required(login_url='home:login')
def create(req):
    if req.method == 'POST':
        form = RecipeForm(req.POST, req.FILES)

        if form.is_valid():
            # Cria instância da receita sem salvar no banco ainda
            recipe = form.save(commit=False)
            recipe.owner = req.user

            # ✅ Formsets já recebem a instância ANTES de validar
            ingredient_formset = IngredientFormSet(
                req.POST,
                prefix='ingredient',
                instance=recipe
            )
            instruction_formset = InstructionFormSet(
                req.POST,
                prefix='instruction',
                instance=recipe
            )

            # Agora valida tudo junto
            if ingredient_formset.is_valid() and instruction_formset.is_valid():
                recipe.save()
                ingredient_formset.save()
                instruction_formset.save()
                return redirect('home:index')

        # Se cair aqui significa que algum formset falhou
        # Precisamos recriar com a instância criada acima
        recipe = Recipe(owner=req.user)
        ingredient_formset = IngredientFormSet(req.POST, prefix='ingredient', instance=recipe)
        instruction_formset = InstructionFormSet(req.POST, prefix='instruction', instance=recipe)

    else:
        form = RecipeForm()
        recipe = Recipe(owner=req.user)
        ingredient_formset = IngredientFormSet(prefix='ingredient', instance=recipe)
        instruction_formset = InstructionFormSet(prefix='instruction', instance=recipe)

    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset,
    }
    return render(req, 'home/create.html', context)


@login_required(login_url='home:login')
def update_recipe(req,recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, owner=req.user)
    
    if req.method == 'POST':
        form = RecipeForm(req.POST, req.FILES, instance=recipe)
        ingredient_formset  = IngredientFormSet(req.POST,instance=recipe, prefix='ingredient')
        instruction_formset  = InstructionFormSet(req.POST,instance=recipe,prefix='instruction')
        
        if form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
            recipe = form.save()
            
            ingredient_formset.save()
            instruction_formset.save()
            return redirect('home:recipe_id',recipe_id= recipe.pk)
        
    else:   
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe,prefix='ingredient')
        instruction_formset  = InstructionFormSet(instance=recipe,prefix='instruction')
        
    context = {
        'form': form,
        'ingredient_formset':ingredient_formset,
        'instruction_formset':instruction_formset,
    }
    
    return render(
        req,
        'home/create.html',
        context
        
    )
    
@login_required(login_url='home:login')
def delete(req,recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id,owner=req.user)
    
    if req.method == 'POST':
        confirmation = req.POST.get('confirmation')
        if confirmation == 'yes':
            recipe.delete()
        return redirect('home:index')
    
    context = {
        'recipe': recipe,
    }
    return render(
        req,
        'home/partial/confirm_delete.html',
        context,
    )