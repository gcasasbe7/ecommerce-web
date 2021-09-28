from ..models import Product

class HighlightManager:

#todo create constructor and init shouldDisplayHighlight to only query the products once

    name = 'Destacados'
    slug = 'destacados'
    absolute_url = f'/shop/{slug}'
    image_url = 'http://127.0.0.1:8000/media/uploads/category_images/destacado.jpeg/'

    @staticmethod
    def getHighlightCategory():
        highlight = {
            'name' : HighlightManager.name,
            'absolute_url' : HighlightManager.absolute_url,
            'image_url' : HighlightManager.image_url,
        }

        return highlight

    @staticmethod
    def getHighlightCategoryDetail():
        highlight = {
            'name' : HighlightManager.name,
            'absolute_url' : HighlightManager.absolute_url,
            'image_url' : HighlightManager.image_url,
            'products' : Product.objects.filter(highlight=True)
        }

        return highlight

    @staticmethod
    def shouldDisplayHighlights():
        if Product.objects.filter(highlight=True):
            return True
        return False