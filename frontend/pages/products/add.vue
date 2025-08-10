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

<template>
  <div class="products-page p-4">
    <div class="mb-8 p-4 border rounded-lg shadow-md">
      <h2 class="text-xl font-semibold mb-3">Tambah Produk Baru</h2>
      <form @submit.prevent="addNewProduct">
        <div class="mb-3">
          <label for="newProductName" class="block text-sm font-medium text-gray-700">Nama Produk</label>
          <input type="text" id="newProductName" v-model="newProductData.name" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <div class="mb-3">
          <label for="newProductDesc" class="block text-sm font-medium text-gray-700">Deskripsi</label>
          <textarea id="newProductDesc" v-model="newProductData.description" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"></textarea>
        </div>
        <div class="mb-3">
          <label for="newProductPrice" class="block text-sm font-medium text-gray-700">Harga</label>
          <input type="number" id="newProductPrice" v-model="newProductData.price" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" step="0.01" required>
        </div>
        <div class="mb-3">
          <label for="newProductStock" class="block text-sm font-medium text-gray-700">Stok</label>
          <input type="number" id="newProductStock" v-model="newProductData.stock" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <div class="mb-3">
          <label for="newProductCategory" class="block text-sm font-medium text-gray-700">Kategori</label>
          <select id="newProductCategory" v-model="newProductData.category" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
            <option :value="null">-- Pilih Kategori --</option>
            <option v-for="cat in productStore.categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
          
        </div>
        <div class="mb-3">
          <label for="newProductImage" class="block text-sm font-medium text-gray-700">Gambar Produk</label>
          <input type="file" id="newProductImage" @change="handleNewImageUpload" accept="image/*" class="mt-1 block w-full">
          <div v-if="imagePreview" class="mt-2">
            <img :src="imagePreview" alt="Image Preview" class="w-32 h-32 object-cover rounded">
          </div>
        </div>
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600" :disabled="productStore.loading">
          {{ productStore.loading ? 'Menambahkan...' : 'Tambah Produk' }}
        </button>
        <p v-if="productStore.error" class="text-red-500 mt-2">{{ productStore.error.message }}</p>
      </form>
    </div>

    <button @click="showAddCategoryModal = true" class="bg-purple-500 text-white font-bold py-2 px-4 rounded hover:bg-purple-600 focus:outline-none focus:shadow-outline w-full md:w-auto mt-2 md:mt-0">
            + Tambah Kategori
          </button>

          <div v-if="showAddCategoryModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-lg font-bold mb-4">Tambah Kategori Baru</h3>
        <form @submit.prevent="submitAddCategory">
          <div class="mb-4">
            <label for="categoryName" class="block text-gray-700 text-sm font-bold mb-2">Nama Kategori:</label>
            <input
              type="text"
              id="categoryName"
              v-model="newCategoryName"
              required
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </div>
          <p v-if="productStore.error" class="text-red-500 text-sm mb-4">{{ productStore.error }}</p>
          <div class="flex justify-end gap-2">
            <button
              type="button"
              @click="showAddCategoryModal = false; newCategoryName = ''; productStore.error = null"
              class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded hover:bg-gray-400 focus:outline-none focus:shadow-outline"
              :disabled="productStore.loading"
            >
              Batal
            </button>
            <button
              type="submit"
              class="bg-green-500 text-white font-bold py-2 px-4 rounded hover:bg-green-600 focus:outline-none focus:shadow-outline"
              :disabled="productStore.loading"
            >
              {{ productStore.loading ? 'Menyimpan...' : 'Simpan' }}
            </button>
          </div>
        </form>
      </div>
    </div>


  </div>
</template>