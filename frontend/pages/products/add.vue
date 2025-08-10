<template>
  <div class="products-page container mx-auto px-4 sm:px-6 lg:px-8 py-6 bg-gray-50 min-h-screen font-sans">

    <div class="flex flex-col md:flex-row justify-between items-center mb-6 gap-4 animate-fade-in">
      <h2 class="text-3xl font-extrabold text-gray-900 flex items-center gap-3">
        <Icon name="mdi:package-variant-closed" class="text-indigo-600 text-4xl" />
        Manajemen Produk
      </h2>
    </div>

    <div class="mb-8 p-6 bg-white rounded-xl shadow-md border border-gray-100 animate-fade-in-down">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Tambah Produk Baru</h2>
      <form @submit.prevent="addNewProduct">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="mb-3 md:mb-0">
            <label for="newProductName" class="block text-sm font-semibold text-gray-700 mb-1">Nama Produk:</label>
            <input type="text" id="newProductName" v-model="newProductData.name" class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base" required>
          </div>
          <div class="mb-3 md:mb-0">
            <label for="newProductPrice" class="block text-sm font-semibold text-gray-700 mb-1">Harga (Rp):</label>
            <input type="number" id="newProductPrice" v-model.number="newProductData.price" class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base" min="0" step="0.01" required>
          </div>
          <div class="mb-3 md:mb-0">
            <label for="newProductStock" class="block text-sm font-semibold text-gray-700 mb-1">Stok:</label>
            <input type="number" id="newProductStock" v-model.number="newProductData.stock" class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base" min="0" required>
          </div>
          <div class="mb-3 md:mb-0">
            <label for="newProductStock" class="block text-sm font-semibold text-gray-700 mb-1">barcode:</label>
            <input type="number" id="newProductStock" v-model.number="newProductData.barcode" class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base" min="0" required>
          </div>
          <div class="mb-3 md:mb-0">
            <label for="newProductCategory" class="block text-sm font-semibold text-gray-700 mb-1">Kategori:</label>
            <select id="newProductCategory" v-model="newProductData.category" class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base" required>
              <option :value="null" disabled>-- Pilih Kategori --</option>
              <option v-for="cat in productStore.categories || []" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div class="mb-3 md:mb-0" v-if="newProductData.category">
            <label for="newProductSubCategory" class="block text-sm font-semibold text-gray-700 mb-1">Sub-Kategori:</label>
            <select
              id="newProductSubCategory"
              v-model="newProductData.subcategory"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base"
              :disabled="!newProductAvailableSubcategories.length"
            >
              <option :value="null">-- Pilih Sub-Kategori (Opsional) --</option>
              <option v-for="subcat in newProductAvailableSubcategories" :key="subcat.id" :value="subcat.id">
                {{ subcat.name }}
              </option>
            </select>
            <p v-if="!newProductAvailableSubcategories.length && newProductData.category" class="text-xs text-gray-500 mt-1">Tidak ada sub-kategori untuk kategori ini.</p>
          </div>
          <div class="col-span-full mb-3">
            <label for="newProductDesc" class="block text-sm font-semibold text-gray-700 mb-1">Deskripsi:</label>
            <textarea id="newProductDesc" v-model="newProductData.description" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-base"></textarea>
          </div>
          <div class="col-span-full mb-4">
            <label for="newProductImage" class="block text-sm font-semibold text-gray-700 mb-1">Gambar Produk:</label>
            <input type="file" id="newProductImage" @change="handleNewImageUpload" accept="image/*" class="w-full text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer">
            <div v-if="imagePreview" class="mt-4 w-32 h-32 overflow-hidden border border-gray-300 rounded-lg shadow-sm">
              <img :src="imagePreview" alt="Image Preview" class="w-full h-full object-cover">
            </div>
          </div>
        </div>

        <button
          type="submit"
          class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold transition-colors duration-200 flex items-center gap-2"
          :disabled="productStore.loading"
        >
          <Icon v-if="productStore.loading" name="mdi:loading" class="animate-spin text-xl" />
          <template v-else><Icon name="mdi:plus-circle-outline" class="text-xl" /> Tambah Produk</template>
        </button>
        <p v-if="productStore.error" class="text-red-600 text-sm mt-3 flex items-center gap-1">
          <Icon name="mdi:alert-circle-outline" /> {{ productStore.error.message }}
        </p>
      </form>
    </div>

    <div class="flex flex-col md:flex-row gap-4 mb-6 animate-fade-in-down">
      <button
        @click="showAddCategoryModal = true"
        class="bg-purple-600 text-white font-bold py-2.5 px-6 rounded-lg shadow-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition duration-200 ease-in-out flex items-center justify-center gap-2 transform active:scale-95"
      >
        <Icon name="mdi:folder-plus-outline" class="text-xl" /> Tambah Kategori
      </button>

      <button
        @click="showAddSubCategoryModal = true"
        class="bg-teal-600 text-white font-bold py-2.5 px-6 rounded-lg shadow-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 transition duration-200 ease-in-out flex items-center justify-center gap-2 transform active:scale-95"
      >
        <Icon name="mdi:folder-multiple-plus-outline" class="text-xl" /> Tambah Sub-Kategori
      </button>
    </div>


  

    
   
    
    <div v-if="showAddCategoryModal" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-xl transform transition-all duration-300 scale-95 opacity-0 animate-scale-in">
        <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Icon name="mdi:folder-plus-outline" class="text-purple-600" /> Tambah Kategori Baru
        </h3>
        <form @submit.prevent="submitAddCategory">
          <div class="mb-4">
            <label for="categoryName" class="block text-gray-700 text-sm font-semibold mb-2">Nama Kategori:</label>
            <input
              type="text"
              id="categoryName"
              v-model="newCategoryName"
              required
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-purple-500 focus:border-purple-500"
            />
          </div>
          <p v-if="productStore.error" class="text-red-600 text-sm mb-4 flex items-center gap-1">
            <Icon name="mdi:alert-circle-outline" /> {{ productStore.error.message }}
          </p>
          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="showAddCategoryModal = false; newCategoryName = ''; productStore.error = null"
              class="px-5 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition-colors duration-200"
              :disabled="productStore.loading"
            >
              Batal
            </button>
            <button
              type="submit"
              class="px-5 py-2 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold transition-colors duration-200 flex items-center gap-2"
              :disabled="productStore.loading"
            >
              <Icon v-if="productStore.loading" name="mdi:loading" class="animate-spin text-xl" />
              <template v-else><Icon name="mdi:content-save-outline" class="text-xl" /> Simpan</template>
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showAddSubCategoryModal" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-xl transform transition-all duration-300 scale-95 opacity-0 animate-scale-in">
        <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Icon name="mdi:folder-multiple-plus-outline" class="text-teal-600" /> Tambah Sub-Kategori Baru
        </h3>
        <form @submit.prevent="submitAddSubCategory">
          <div class="mb-4">
            <label for="subCategoryName" class="block text-gray-700 text-sm font-semibold mb-2">Nama Sub-Kategori:</label>
            <input
              type="text"
              id="subCategoryName"
              v-model="newSubCategoryData.name"
              required
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-teal-500 focus:border-teal-500"
            />
          </div>
          <div class="mb-4">
            <label for="subCategoryParent" class="block text-gray-700 text-sm font-semibold mb-2">Kategori Induk:</label>
            <select
              id="subCategoryParent"
              v-model="newSubCategoryData.category"
              required
              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-teal-500 focus:border-teal-500"
            >
              <option :value="null" disabled>-- Pilih Kategori Induk --</option>
              <option v-for="cat in productStore.categories || []" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>
          <p v-if="productStore.error" class="text-red-600 text-sm mb-4 flex items-center gap-1">
            <Icon name="mdi:alert-circle-outline" /> {{ productStore.error.message }}
          </p>
          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="showAddSubCategoryModal = false; newSubCategoryData.name = ''; newSubCategoryData.category = null; productStore.error = null"
              class="px-5 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition-colors duration-200"
              :disabled="productStore.loading"
            >
              Batal
            </button>
            <button
              type="submit"
              class="px-5 py-2 rounded-lg bg-teal-600 text-white hover:bg-teal-700 font-semibold transition-colors duration-200 flex items-center gap-2"
              :disabled="productStore.loading"
            >
              <Icon v-if="productStore.loading" name="mdi:loading" class="animate-spin text-xl" />
              <template v-else><Icon name="mdi:content-save-outline" class="text-xl" /> Simpan</template>
            </button>
          </div>
        </form>
      </div>
    </div>  

  </div>
</template>
<script setup>
import { ref, onMounted, reactive, computed, watch } from 'vue';
import { useProductStore } from '@/store/products';
import { useRuntimeConfig } from '#app';

const productStore = useProductStore();
const runtimeConfig = useRuntimeConfig();

// --- State untuk Modal Kategori & Sub-Kategori ---
const showAddCategoryModal = ref(false);
const showAddSubCategoryModal = ref(false);

// --- Data untuk Form Produk Baru ---
const newProductData = reactive({
  name: '',
  description: '',
  price: 0,
  stock: 0,
  barcode:0,
  category: null,
  subcategory: null, // <--- BARU: Tambahkan field subcategory
  image: null // Ini akan menampung File object
});
const imagePreview = ref(null);

// --- Data untuk Form Kategori Baru ---
const newCategoryName = ref('');

// --- Data untuk Form Sub-Kategori Baru ---
const newSubCategoryData = reactive({
  name: '',
  category: null, // ID kategori induk
});

// --- Fungsi untuk Upload Gambar Produk Baru ---
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

// --- Pemuatan Data Awal ---




// --- Computed Property untuk Sub-Kategori yang Tersedia untuk Filter ---


// --- Computed Property untuk Sub-Kategori yang Tersedia untuk Form Produk Baru ---
// Ini penting agar dropdown sub-kategori di form produk baru hanya menampilkan yang relevan
const newProductAvailableSubcategories = computed(() => {
  if (!productStore.categories || !newProductData.category) {
    return [];
  }
  return productStore.getSubcategoriesByCategoryId(newProductData.category);
});


// --- Watcher untuk Filter ---
const searchQuery = ref('');
const selectedSubCategory = ref('');
const selectedCategory = ref('');

watch(selectedCategory, (newCategoryId) => {
  selectedSubCategory.value = '';
  applyProductFilters();
});

watch(selectedSubCategory, () => {
  applyProductFilters();
});

watch(searchQuery, () => {
  applyProductFilters();
});

// --- Watcher untuk form produk baru: reset subcategory jika kategori induk berubah ---
watch(() => newProductData.category, (newCategoryId, oldCategoryId) => {
  // Hanya reset jika kategori berubah dan bukan dari null ke suatu nilai
  if (newCategoryId !== oldCategoryId) {
    newProductData.subcategory = null;
  }
});


const applyProductFilters = async () => {
  const filters = {};
  if (selectedCategory.value) {
    filters.category = parseInt(selectedCategory.value);
  }
  if (selectedSubCategory.value) {
    filters.sub_category = parseInt(selectedSubCategory.value);
  }
  if (searchQuery.value) {
    filters.search = searchQuery.value;
  }
  console.log('Applying filters:', filters);
  await productStore.fetchProducts(filters);
};

// --- Fungsi untuk Mendapatkan URL Gambar ---

// --- Fungsi untuk Menangani Error Gambar ---


// --- Fungsi untuk Menambah Produk Baru ---
const addNewProduct = async () => {
  productStore.error = null;
  productStore.loading = true;
  try {
    const formData = new FormData();
    formData.append('name', newProductData.name);
    formData.append('description', newProductData.description);
    formData.append('price', newProductData.price);
    formData.append('stock', newProductData.stock);
    formData.append('barcode', newProductData.barcode);
    
    if (newProductData.category !== null) {
      formData.append('category', newProductData.category);
    }
    // <--- BARU: Tambahkan sub_category ke FormData jika ada
    if (newProductData.subcategory !== null) {
      formData.append('sub_category', newProductData.subcategory);
    }

    if (newProductData.image) {
      formData.append('image', newProductData.image);
    }

    const success = await productStore.addProduct(formData);
    if (success) {
      // Reset form data
      newProductData.name = '';
      newProductData.description = '';
      newProductData.price = 0;
      newProductData.stock = 0;
      newProductData.barcode = 0;

      newProductData.category = null;
      newProductData.subcategory = null; // <--- BARU: Reset subcategory
      newProductData.image = null;
      imagePreview.value = null;
      await productStore.fetchProducts(); // Refresh product list
    }
  } catch (error) {
    console.error("Error adding product:", error);
  } finally {
    productStore.loading = false;
  }
};

// --- Fungsi untuk Menambah Kategori Baru ---
const submitAddCategory = async () => {
  if (!newCategoryName.value.trim()) {
    productStore.error = 'Nama kategori tidak boleh kosong.';
    return;
  }
  const success = await productStore.addCategory(newCategoryName.value);
  if (success) {
    newCategoryName.value = '';
    showAddCategoryModal.value = false;
    await productStore.fetchCategories();
  }
};

// --- Fungsi untuk Menambah Sub-Kategori Baru ---
const submitAddSubCategory = async () => {
  if (!newSubCategoryData.name.trim()) {
    productStore.error = 'Nama sub-kategori tidak boleh kosong.';
    return;
  }
  if (!newSubCategoryData.category) {
    productStore.error = 'Pilih kategori induk untuk sub-kategori ini.';
    return;
  }

  const payload = {
    name: newSubCategoryData.name,
    category: newSubCategoryData.category,
  };

  const success = await productStore.addSubCategory(payload);
  if (success) {
    newSubCategoryData.name = '';
    newSubCategoryData.category = null;
    showAddSubCategoryModal.value = false;
    await productStore.fetchCategories();
  }
};

// --- Fungsi untuk Refresh Data ---

// --- Ambil produk dan kategori saat komponen dimuat ---
onMounted(async () => {
  await productStore.fetchCategories(); // Muat kategori dulu
  await productStore.fetchProducts(); // Kemudian muat produk
});
</script>

<style scoped>
/* Main page container styling */
.products-page {
  /* No specific height, allow content to define */
}

/* Product Card Styling */
.product-card {
  @apply bg-white border border-gray-200 rounded-xl shadow-lg
          flex flex-col overflow-hidden cursor-pointer
          transform hover:scale-[1.02] transition-all duration-300 ease-in-out;
  min-height: 420px; /* Adjust as needed for consistent card height */
}

.product-image-wrapper {
  @apply w-full h-48; /* Consistent image height */
}

.product-image {
  @apply w-full h-full object-cover transform transition-transform duration-300 group-hover:scale-105;
}

.product-name {
  display: -webkit-box;
  -webkit-line-clamp: 2; /* Limit to 2 lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 2.5em; /* Space for 2 lines */
}

.product-category {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Stock Badge Animations */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .7;
  }
}
.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Modal Animations */
@keyframes scale-in {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
.animate-scale-in {
  animation: scale-in 0.3s ease-out forwards;
}

/* Loading Spinner */
.loader-lg {
  border: 6px solid #e0e0e0;
  border-top: 6px solid #6366f1; /* Indigo color */
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 1.5s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* General Fade-in for sections */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
.animate-fade-in {
  animation: fade-in 0.4s ease-out forwards;
}

/* Fade-in-down animation for filter section */
@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-down {
  animation: fade-in-down 0.5s ease-out forwards;
}
</style>