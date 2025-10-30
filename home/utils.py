from home.models import Favorite

def get_user_favorites(req):
    if not req.session.session_key:
        req.session.save()
        
    session_key = req.session.session_key
    return set(Favorite.objects.filter(session_key=session_key).values_list('recipe_id', flat=True))