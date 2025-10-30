from home.models import Category

def default_context(request):
    return {
        'categories' : Category.objects.all()
    }