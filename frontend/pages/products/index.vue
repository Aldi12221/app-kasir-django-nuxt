<template>
  <div class="products-page p-4">
   
          

    <h2 class="text-xl font-semibold mb-3">Daftar Produk</h2>
    <div v-if="productStore.loading">Loading products...</div>
    <div v-else-if="productStore.error" class="text-red-500">{{ productStore.error.message }}</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="product in productStore.products" :key="product.id" class="product-card border p-4 rounded-lg shadow-md">
        <img v-if="product.image" :src="product.image" :alt="product.name" class="w-full h-48 object-cover rounded-md mb-2">
        <div v-else class="w-full h-48 bg-gray-200 flex items-center justify-center rounded-md mb-2">
            <span class="text-gray-500">No Image</span>
        </div>
        <h3 class="text-lg font-bold">{{ product.name }}</h3>
        <p class="text-gray-600">Rp {{ product.price }}</p>
        <p class="text-sm text-gray-500">Stok: {{ product.stock }}</p>
        <p class="text-sm text-gray-500">Kategori: {{ product.category_name || 'N/A' }}</p>
        <div class="mt-3">
          <NuxtLink :to="`/products/${product.id}`" class="px-3 py-1 bg-yellow-500 text-white rounded-md hover:bg-yellow-600 mr-2">Edit</NuxtLink>
          <button @click="confirmDelete(product.id)" class="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600">Hapus</button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>

import { ref, onMounted, reactive } from 'vue';
import { useProductStore } from '@/store/products';

const productStore = useProductStore();
const runtimeConfig = useRuntimeConfig();
const showAddCategoryModal = ref(false);

// Data untuk form produk baru
const newProductData = reactive({
    name: '',
    description: '',
    price: 0,
    stock: 0,
    category: null,
    image: null // Ini akan menampung File object
});
const imagePreview = ref(null);

const handleNewImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        newProductData.image = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        newProductData.image = null;
        imagePreview.value = null;
    }
};



// Fungsi untuk mendapatkan URL gambar yang lengkap
const productImageUrl = (relativePath) => {
    if (relativePath) {
        return `${runtimeConfig.public.mediaBaseUrl}${relativePath}`;
    }
    return ''; // Atau URL placeholder
};
const newCategoryName = ref('');
const submitAddCategory = async () => {
  if (!newCategoryName.value.trim()) {
    productStore.error = 'Nama kategori tidak boleh kosong.';
    return;
  }
  const success = await productStore.addCategory(newCategoryName.value);
  if (success) {
    newCategoryName.value = '';
    showAddCategoryModal.value = false;
  }
};

// Ambil produk dan kategori saat komponen dimuat
onMounted(async () => {
  await productStore.fetchCategories();
  await productStore.fetchProducts();
});
</script>