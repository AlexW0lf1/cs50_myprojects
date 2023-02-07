from .models import Lot

def categories_processor(request):
    categories = Lot.CATEGORIES
    return {'categories': categories,}