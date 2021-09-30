from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Q
from ..models import Product, Category
from ..serializers import ProductSerializer, CategorySerializer, CategoryShopListSerializer
from ..managers.response_manager import ResponseManager
from ..managers.highlight_manager import HighlightManager

'''
Shop Product Detail View
- Returns a detailed product with all it's data
Allowed HTTP methods: GET
Requires authentication: NO
'''
class ShopProductDetail(APIView):
    
    def get_object(self, product_slug, category_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_slug, category_slug, format=None):
        product = self.get_object(product_slug, category_slug)

        if product:
            serializer = ProductSerializer(product)

            if serializer.is_valid:
                return ResponseManager.build_successful_response({
                    'product': serializer.data
                })
            else:
                return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, "There has been an issue with the product you are trying to view. Please try again later.")

        return ResponseManager.build_invalid_response(status.HTTP_404_NOT_FOUND, "Product not found. Please try again later.")

'''
Shop Categories List View
- Returns all the available categories to be displayed within the shop including Highlight section if valid
Allowed HTTP methods: GET
Requires authentication: NO
'''
class CategoriesList(APIView):
    
    def get(self, request, format=None):
        categories = Category.objects.filter(visible=True)
        serializer = CategoryShopListSerializer(categories, many=True)

        if serializer.is_valid:
            return ResponseManager.build_successful_response({
                'categories': serializer.data,
                'highlight': HighlightManager.getHighlightCategory() if HighlightManager.shouldDisplayHighlights() else ''
            })
        else:
            return ResponseManager.build_invalid_response(
                status.HTTP_406_NOT_ACCEPTABLE, 
                "There has been an issue with some category you are trying to view. Please try again later."
            )

'''
Shop Category Detail View
- Returns a detailed category with all it's data. Also returns all the current available categories for the shop navigation
Allowed HTTP methods: GET
Requires authentication: NO
'''
class ShopCategoryDetail(APIView):

    def get_object(self, category_slug):
        try:
            # Are we trying to fetch the detail for the Highlighted section?
            if category_slug == HighlightManager.slug:
                return HighlightManager.getHighlightCategoryDetail()
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return None

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        all_categories = Category.objects.filter(visible=True)

        if category:
            serializer = CategorySerializer(category)
            all_categories_serializer = CategoryShopListSerializer(all_categories, many=True)
            categories_data = all_categories_serializer.data

            # Do we have any highlighted products to display?
            if HighlightManager.shouldDisplayHighlights():
                categories_data.insert(0, HighlightManager.getHighlightCategory())

            if serializer.is_valid:
                return ResponseManager.build_successful_response({
                    'category_detail': serializer.data,
                    'all_categories': categories_data
                })
            else:
                return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, 
                    "There has been an issue fetching the category you are trying to view. Please try again later.")

        return ResponseManager.build_invalid_response(status.HTTP_404_NOT_FOUND, 
            "Category not found. Please try again later.")

'''
Shop Search View
- Returns a list with the products that match the criteria of the given search parameters
Allowed HTTP methods: POST
Requires authentication: NO
'''
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)

        if serializer.is_valid:
            return ResponseManager.build_successful_response({
                'result': serializer.data
            })
    else:
        return ResponseManager.build_successful_response({})