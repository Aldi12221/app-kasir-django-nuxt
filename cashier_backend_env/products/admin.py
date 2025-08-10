# cashier_backend/your_app_name/admin.py

from django.contrib import admin
from .models import Category, SubCategory, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    list_filter = ('category',)
    search_fields = ('name',)
    # autocomplete_fields = ['category'] # Opsional: jika Category Anda punya banyak data

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sub_category', 'price', 'stock', 'is_active', 'created_at',)
    list_filter = ('category', 'sub_category', 'is_active',) # Tambahkan sub_category di filter admin
    search_fields = ('name', 'description','barcode')
    # formfield_overrides = { # Opsional: Untuk memilih sub_category berdasarkan category yang dipilih (lebih kompleks)
    #     models.ForeignKey: {'widget': forms.Select(attrs={'onchange': 'filterSubCategories(this)'})}
    # }

    # Ini yang penting untuk form add/edit product di admin:
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'stock', 'image', 'is_active','barcode')
        }),
        ('Kategori', {
            'fields': ('category', 'sub_category') # Pastikan sub_category ada di sini
        }),
        ('Info Tanggal', {
            'fields': ('order_date', 'created_at', 'updated_at'),
            'classes': ('collapse',) # Opsional: untuk menyembunyikan secara default
        }),
    )
    readonly_fields = ('order_date', 'created_at', 'updated_at',)

    # Anda bisa menambahkan JavaScript kustom untuk memfilter sub_category berdasarkan category
    # Diperlukan file admin/js/dynamic_subcategories.js
    # class Media:
    #     js = ('admin/js/dynamic_subcategories.js',)