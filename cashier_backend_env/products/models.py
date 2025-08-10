from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    # Menghubungkan SubCategory ke Category
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        # Memastikan nama subkategori unik dalam kategori yang sama
        unique_together = ('name', 'category')
        verbose_name_plural = "SubCategories"
        ordering = ['category__name', 'name']

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=60, decimal_places=2 ,default=0.00)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products_by_subcategory')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) # Perlu Pillow: pip install Pillow
    is_active = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True) # Otomatis mengisi tanggal dan waktu saat dibuat
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
    

    def __str__(self):
        return self.name