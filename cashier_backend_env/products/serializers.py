from rest_framework import serializers
from .models import Category, Product, SubCategory # Pastikan semua model diimpor

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # --- PERUBAHAN UTAMA DI SINI ---
    # Untuk field yang akan menerima ID dari frontend (saat menulis/POST/PUT)
    # Anda perlu PrimaryKeyRelatedField TANPA read_only=True dan dengan queryset.
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all() # Penting: Beri tahu serializer dari mana mengambil objek Category
    )
    sub_category = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), # Penting: Beri tahu serializer dari mana mengambil objek SubCategory
        allow_null=True,                    # Izinkan null jika model Anda mengizinkan (seperti yang sudah ada di models.py)
        required=False                      # Tandai sebagai tidak wajib jika model Anda mengizinkan
    )
    # --- AKHIR PERUBAHAN UTAMA ---

    # Field-field ini SANGAT BAIK untuk tampilan (saat membaca/GET)
    # Mereka read_only=True dan mengambil nama dari relasi.
    category_name = serializers.CharField(source='category.name', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True, allow_null=True) # Tambahkan allow_null=True

    # Price Field: Ini sudah benar, pastikan sesuai dengan model Anda.
    price = serializers.DecimalField(max_digits=60, decimal_places=2, localize=False)
    
    # Image Field: Ini juga sudah benar untuk menerima file.
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta: 
        model = Product
        # Gunakan '__all__' atau daftar eksplisit semua field,
        # Pastikan 'category' dan 'sub_category' (bukan category_name/sub_category_name)
        # ADA di daftar ini jika Anda menggunakan daftar eksplisit.
        fields = '__all__' # Ini akan menyertakan 'category' dan 'sub_category' yang dapat ditulis

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Logika ini untuk mengubah path gambar menjadi URL lengkap saat membaca data.
        if instance.image:
            request = self.context.get('request')
            if request is not None:
                representation['image'] = request.build_absolute_uri(instance.image.url)
            else:
                representation['image'] = instance.image.url
        # Jika instance.sub_category adalah None, pastikan sub_category_name juga None
        # Ini akan otomatis dihandle oleh `source='sub_category.name', read_only=True, allow_null=True`
        return representation