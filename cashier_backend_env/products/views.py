# cashier_backend/products/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Import custom permissions
from cashier_backend.permissions import IsAdminUser, IsCashierOrAdmin 
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


from rest_framework.filters import SearchFilter, OrderingFilter
# Import DjangoFilterBackend jika Anda menggunakan django-filter
# from django_filters.rest_framework import DjangoFilterBackend


from .models import Category,SubCategory, Product
from .serializers import CategorySerializer, ProductSerializer, SubCategorySerializer

# --- CategoryViewSet (Tidak ada perubahan signifikan yang diperlukan untuk masalah produk) ---
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser] # Default, akan ditimpa get_permissions

    def get_permissions(self):
        # Prioritaskan Admin/Superuser agar selalu memiliki akses penuh
        if (self.request.user.is_authenticated and 
            (self.request.user.is_superuser or self.request.user.groups.filter(name='admin').exists())):
            return [IsAuthenticated()] 

        # Jika bukan Admin, terapkan izin khusus:
        if self.action in ['list', 'retrieve']: 
            permission_classes = [IsAuthenticated, IsCashierOrAdmin]
        else: # Untuk create, update, delete kategori
            permission_classes = [IsAuthenticated, IsAdminUser]
        
        return [permission() for permission in permission_classes]

# --- SubCategoryViewSet (Perbaikan kecil pada group name) ---
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated, IsCashierOrAdmin] 
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        
        if category_id:
            try:
                queryset = queryset.filter(category_id=int(category_id))
            except ValueError:
                pass 
        return queryset
    
    def get_permissions(self):
        if (self.request.user.is_authenticated and 
            (self.request.user.is_superuser or self.request.user.groups.filter(name='admin').exists())): # <--- Pastikan 'Admin' konsisten
            return [IsAuthenticated()] 

        if self.action in ['list', 'retrieve', 'create']: 
            permission_classes = [IsAuthenticated, IsCashierOrAdmin]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser] 

        return [permission() for permission in permission_classes] 

# --- ProductViewSet (Fokus utama perbaikan) ---
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # Gunakan filter_backends untuk SearchFilter dan OrderingFilter bawaan DRF
    filter_backends = [SearchFilter, OrderingFilter] 
    search_fields = ['name', 'description','barcode']
    ordering_fields = ['name', 'price', 'stock', 'created_at']
    filterset_fields = ['category', 'sub_category', 'is_active', 'barcode'] # Tambahkan 'barcode' ke filterable fields

    # Jika Anda ingin filter category dan sub_category menggunakan django-filter,
    # Anda akan mendefinisikan FilterSet di sini dan menambahkan DjangoFilterBackend.
    # Namun, karena Anda sudah punya logika manual di get_queryset, kita bisa gabungkan.

    def get_queryset(self):
        queryset = super().get_queryset() # Dapatkan queryset dasar
        
        # Filter berdasarkan category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter berdasarkan sub_category
        sub_category_id = self.request.query_params.get('sub_category')
        if sub_category_id:
            queryset = queryset.filter(sub_category_id=sub_category_id)
            
        # Filter berdasarkan is_active
        is_active = self.request.query_params.get('is_active')
        if is_active is not None: # Cek jika parameter ada
            # Konversi string 'true'/'false' ke boolean
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)

        # Filter berdasarkan search query (name, description, barcode)
        search_query = self.request.query_params.get('search')
        if search_query:
           
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(barcode__icontains=search_query)
            )
            
        # Filter berdasarkan barcode spesifik (jika ada di query params, bukan action)
        barcode_param = self.request.query_params.get('barcode')
        if barcode_param:
            queryset = queryset.filter(barcode=barcode_param)
    @action(detail=False, methods=['get'], url_path='by-barcode/(?P<barcode_value>[^/.]+)')
    def by_barcode(self, request, barcode_value=None):
        try:
            product = self.get_queryset().get(barcode=barcode_value)
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'detail': 'Product with this barcode not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        # Ambil queryset dasar dari ModelViewSet
        queryset = super().get_queryset()

        # --- Filter Kustom untuk Kategori dan Sub-Kategori ---
        # Ini akan bekerja bersama dengan SearchFilter dan OrderingFilter bawaan DRF
        # (Filter bawaan DRF akan diterapkan *setelah* get_queryset dieksekusi)
        
        category_id = self.request.query_params.get('category')
        if category_id:
            try:
                queryset = queryset.filter(category_id=int(category_id))
            except ValueError:
                pass 

        sub_category_id = self.request.query_params.get('sub_category')
        if sub_category_id:
            try:
                queryset = queryset.filter(sub_category_id=int(sub_category_id))
            except ValueError:
                pass 
        
        # Hapus filter pencarian dan pengurutan manual di sini
        # karena sudah ditangani oleh `filter_backends` di atas.
        # search_query = self.request.query_params.get('search')
        # ...
        # ordering_param = self.request.query_params.get('ordering')
        # ...

        return queryset

    def get_permissions(self):
        if (self.request.user.is_authenticated and 
            (self.request.user.is_superuser or self.request.user.groups.filter(name='admin').exists())):
            return [IsAuthenticated()] 
        
        if self.action in ['list', 'retrieve','by_barcode']: 
            permission_classes = [IsAuthenticated, IsCashierOrAdmin]
        else: # create, update, delete
            permission_classes = [IsAuthenticated, IsAdminUser] 
        
        return [permission() for permission in permission_classes]