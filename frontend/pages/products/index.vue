<template>
  <div class="products-page p-4">
   
          

    <h2 class="text-xl font-semibold mb-3">Daftar Produk</h2>

    <div class="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto flex-wrap justify-end">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Cari nama produk..."
              class="flex-1 min-w-[150px] w-full sm:w-64 px-4 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 text-base placeholder-gray-500 transition duration-200"
            />
            <button
              @click="openBarcodeScanner"
              class="w-full sm:w-auto flex-shrink-0 px-3 py-2 md:px-4 md:py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition duration-200 ease-in-out transform active:scale-95 flex items-center justify-center gap-1 md:gap-2 text-sm md:text-base"
            >
              <Icon name="mdi:barcode-scan" class="text-lg md:text-xl" /> Scan Barcode
            </button>
            <select
              v-model="selectedCategory"
              class="flex-1 min-w-[120px] w-full sm:w-48 px-4 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 text-base transition duration-200"
            >
              <option value="">Semua Kategori</option>
              <option v-for="category in productStore.categories || []" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>

            <select
              v-model="selectedSubCategory"
              v-if="availableSubcategories && availableSubcategories.length > 0"
              class="flex-1 min-w-[120px] w-full sm:w-48 px-4 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 text-base transition duration-200"
            >
              <option value="">Semua Sub-Kategori</option>
              <option v-for="subcat in availableSubcategories" :key="subcat.id" :value="subcat.id">
                {{ subcat.name }}
              </option>
            </select>
          </div>
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
          <button @click="deleteProduct(product.id)" class="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600">Hapus</button>
        </div>
      </div>
    </div>
    
  </div>
   <Modal :is-open="isScannerModalOpen" @close="closeBarcodeScanner">
      <h3 class="text-xl md:text-2xl font-bold text-gray-800 mb-4 text-center">Pindai Barcode Produk</h3>
      <BarcodeScanner 
        :is-active="isScannerModalOpen" 
        @scan-success="handleBarcodeScanSuccess" 
        @scan-error="handleBarcodeScanError"
      />
      <div v-if="scanMessage" :class="{'text-green-600': scanMessageType === 'success', 'text-red-600': scanMessageType === 'error'}" class="text-center mt-4 text-sm md:text-base">
        {{ scanMessage }}
      </div>
      <div class="flex justify-center mt-6">
        <button @click="closeBarcodeScanner" class="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100 transition duration-200 text-sm md:text-base">
          Tutup Pemindai
        </button>
      </div>
    </Modal>
</template>

<script setup>

import { ref, onMounted, reactive } from 'vue';
import { useProductStore } from '@/store/products';

const productStore = useProductStore();

const searchQuery = ref('');
const selectedCategory = ref('');

const selectedSubCategory = ref('');


// Data untuk form produk baru

const availableSubcategories = computed(() => {
  if (!productStore.categories || !selectedCategory.value) {
    return [];
  }
  return productStore.getSubcategoriesByCategoryId(selectedCategory.value);
});
const { pending: categoriesDataLoading, error: categoriesDataError } = useAsyncData(
  'initial-categories',
  async () => {
    await productStore.fetchCategories();
  },
  {
    server: true,
    lazy: false,
  }
);

const deleteProduct = async (productId) => {
  if (confirm('Anda yakin ingin menghapus produk ini?')) {
    // Logika untuk delete produk (Anda perlu menambahkan aksi deleteProduct di store)
    const success = await productStore.deleteProduct(productId);
    if (success) {
      productStore.fetchProducts(); // Refresh list
    }
    console.log("Delete product logic needed for ID:", productId);
  }
};
watch(selectedCategory, () => {
  selectedSubCategory.value = '';
  applyProductFilters();
});

// Watcher untuk memicu filter produk saat sub-kategori berubah
watch(selectedSubCategory, () => {
  applyProductFilters();
});

// Watcher untuk memicu filter produk saat search query berubah
watch(searchQuery, () => {
  applyProductFilters();
});

// --- Fungsi untuk Menerapkan Filter Produk ---
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

// Fungsi untuk mendapatkan URL gambar yang lengkap

const newCategoryName = ref('');


// Ambil produk dan kategori saat komponen dimuat
onMounted(async () => {
  await productStore.fetchCategories();
  await productStore.fetchProducts();
});
const isScannerModalOpen = ref(false); 
const scanMessage = ref(''); 
const scanMessageType = ref(''); 

const openBarcodeScanner = () => {
  isScannerModalOpen.value = true;
  scanMessage.value = ''; 
  scanMessageType.value = '';
};

const closeBarcodeScanner = () => {
  isScannerModalOpen.value = false;
  scanMessage.value = ''; 
  scanMessageType.value = '';
};

const handleBarcodeScanSuccess = async (barcode) => {
  scanMessage.value = `Barcode terdeteksi: ${barcode}. Mencari produk...`;
  scanMessageType.value = 'success';
  try {
    // LANGSUNG SET searchQuery dengan barcode
    searchQuery.value = barcode; 
    
    // Tutup modal scanner segera setelah barcode dipindai
    closeBarcodeScanner(); 
    
    // Pesan sukses akan ditampilkan di input search atau di katalog
    // Tidak perlu lagi memanggil API di sini, karena watcher searchQuery akan memicu applyProductFilters
    // dan backend akan melakukan pencarian berdasarkan barcode yang ada di searchQuery.
    scanMessage.value = `Pencarian untuk barcode "${barcode}" diterapkan.`;
    scanMessageType.value = 'success';

  } catch (error) {
    console.error('Error handling barcode scan:', error);
    scanMessage.value = `Gagal mencari produk: ${error.message}`;
    scanMessageType.value = 'error';
  }
};

const handleBarcodeScanError = (err) => {
  scanMessage.value = `Gagal memindai: ${err}`;
  scanMessageType.value = 'error';
};

</script>