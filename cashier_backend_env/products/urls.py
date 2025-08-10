from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, SubCategoryViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'products', ProductViewSet) # Pastikan ini ada
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Endpoint best_sellers akan otomatis terdaftar sebagai /   /products/best_sellers/
    # karena kita menggunakannya sebagai @action pada ProductViewSet.
]