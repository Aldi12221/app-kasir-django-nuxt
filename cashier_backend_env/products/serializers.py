from rest_framework import serializers
from .models import Category, Product,SubCategory

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__' # Akan menyertakan id dan name SubCategory



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True, source='category.id')
    # Field 'category' tetap mengembalikan ID numerik dari kategori utama
    
    category_name = serializers.CharField(source='category.name', read_only=True)

    # Tambahkan field untuk sub-kategori
    sub_category = serializers.PrimaryKeyRelatedField(read_only=True, source='sub_category.id') # ID sub-kategori
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True) # Nama sub-kategori
    
    # Optional: tetap sertakan nama kategori jika Anda butuh untuk tampilan lain
    
    # Tambahkan ini untuk memastikan price dikirim sebagai string numerik jika bukan Decimal
    # Atau jika Anda menggunakan FloatField, tidak perlu ini.
    price = serializers.DecimalField(max_digits=10, decimal_places=2, localize=False)
    
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            request = self.context.get('request')
            if request is not None:
                representation['image'] = request.build_absolute_uri(instance.image.url)
            else:
                representation['image'] = instance.image.url
        return representation