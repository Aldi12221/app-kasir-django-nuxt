<template>
  <div class="container mx-auto px-4 py-4 md:py-8 flex flex-col gap-4 md:gap-8 bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen font-sans">
    
    <div class="bg-white p-6 rounded-2xl shadow-xl border border-gray-100 transform hover:scale-[1.005] transition-transform duration-200 min-w-0">
      <h2 class="text-2xl font-bold text-gray-800 mb-5 flex items-center gap-3">
        <Icon name="mdi:chart-line-variant" class="text-teal-600 text-3xl" />
        Ringkasan Penjualan
        <span class="text-blue-500 text-base font-semibold ml-auto">{{ dailySummary.dateRange }}</span>
      </h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6 items-end">
        <div>
          <label for="tanggalMulai" class="block text-sm font-semibold text-gray-700 mb-1">Dari Tanggal:</label>
          <input
            type="date"
            id="tanggalMulai"
            v-model="tanggalMulai"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 transition duration-200 text-base"
          >
        </div>
        <div>
          <label for="tanggalAkhir" class="block text-sm font-semibold text-gray-700 mb-1">Sampai Tanggal:</label>
          <input
            type="date"
            id="tanggalAkhir"
            v-model="tanggalAkhir"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 transition duration-200 text-base"
          >
        </div>
        <button
          @click="refreshDailySummary"
          class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 px-6 rounded-lg shadow-md transition duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center justify-center gap-2 transform active:scale-95"
        >
          <Icon name="mdi:calendar-search" class="text-xl" /> Tampilkan Data
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-blue-50 p-5 rounded-xl shadow-inner flex flex-col items-start border border-blue-100 group">
          <Icon name="mdi:cash-multiple" class="text-blue-500 text-4xl mb-2 group-hover:scale-110 transition-transform" />
          <h3 class="text-base font-medium text-blue-800">Total Penjualan</h3>
          <p class="text-3xl font-bold text-blue-900 mt-1">Rp {{ dailySummary.totalSales?.toLocaleString('id-ID') || '0' }}</p>
        </div>
        <div class="bg-green-50 p-5 rounded-xl shadow-inner flex flex-col items-start border border-green-100 group">
          <Icon name="mdi:receipt-text-outline" class="text-green-500 text-4xl mb-2 group-hover:scale-110 transition-transform" />
          <h3 class="text-base font-medium text-green-800">Jumlah Transaksi</h3>
          <p class="text-3xl font-bold text-green-900 mt-1">{{ dailySummary.totalOrders?.toLocaleString('id-ID') || '0' }}</p>
        </div>
        <div class="bg-orange-50 p-5 rounded-xl shadow-inner flex flex-col items-start border border-orange-100 group">
          <Icon name="mdi:package-variant-closed" class="text-orange-500 text-4xl mb-2 group-hover:scale-110 transition-transform" />
          <h3 class="text-base font-medium text-orange-800">Produk Stok Rendah</h3>
          <p class="text-3xl font-bold text-orange-900 mt-1">{{ lowStockProducts.length }}</p>
        </div>
      </div>
    </div>

    <div class="flex flex-col lg:flex-row gap-4 md:gap-8">
      <div class="flex-1 flex flex-col gap-4 md:gap-6 min-w-0">
        <!-- Low Stock Alert -->
        <div v-if="showLowStockAlert" class="bg-gradient-to-r from-yellow-50 to-orange-50 border-l-4 border-orange-400 text-orange-800 p-4 rounded-lg shadow-md flex items-start gap-4 animate-slide-in-down overflow-x-auto custom-scrollbar" role="alert">
          <Icon name="mdi:alert-rhombus-outline" class="text-orange-600 text-3xl flex-shrink-0 animate-pulse" />
          <div>
            <p class="font-bold text-xl mb-1">Perhatian Penting: Stok Hampir Habis!</p>
            <p class="text-sm">Produk-produk berikut memerlukan perhatian segera untuk restock:</p>
            <ul class="list-disc list-inside text-sm mt-3 max-h-28 overflow-y-auto pr-2 custom-scrollbar">
              <li v-for="product in lowStockProducts" :key="product.id" class="py-0.5">
                <span class="font-semibold">{{ product.name }}</span> (Sisa Stok: <span class="text-red-600 font-bold">{{ product.stock }}</span>)
              </li>
            </ul>
          </div>
        </div>

        <div class="bg-white p-4 md:p-6 rounded-xl shadow-xl border border-gray-100 transform hover:scale-[1.005] transition-transform duration-200 min-w-0 flex flex-col">
          <h2 class="text-lg md:text-2xl font-bold text-gray-800 mb-3 md:mb-5 flex items-center gap-1 md:gap-2">
            <Icon name="mdi:tag-multiple-outline" class="text-xl md:text-3xl text-purple-600" />
            Katalog Produk
          </h2>

          <!-- Input Pencarian & Filter -->
          <div class="flex flex-col sm:flex-row items-center gap-2 md:gap-3 mb-3 md:mb-5">
            <div class="relative flex-1 w-full">
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Cari produk dengan nama atau deskripsi..."
                class="pl-8 pr-3 py-2 md:pl-10 md:pr-4 md:py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm md:text-base placeholder-gray-500 w-full transition duration-200"
              />
              <Icon name="mdi:magnify" class="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400 text-lg md:text-xl" />
            </div>

            
            

            <select
              v-model="selectedCategory"
              class="w-full sm:w-auto flex-shrink-0 px-3 py-2 md:px-4 md:py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm md:text-base text-gray-700 transition duration-200"
            >
              <option value="">Semua Kategori</option>
              <option v-for="category in productStore.categories || []" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>

            <select
              v-model="selectedSubCategory"
              v-if="availableSubcategories.length > 0"
              class="w-full sm:w-auto flex-shrink-0 px-3 py-2 md:px-4 md:py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm md:text-base text-gray-700 transition duration-200"
            >
              <option value="">Semua Sub-Kategori</option>
              <option v-for="subcat in availableSubcategories" :key="subcat.id" :value="subcat.id">
                {{ subcat.name }}
              </option>
            </select>
          </div>

          <!-- Produk -->
          <div v-if="productStore.loading || categoriesDataLoading" class="text-center text-gray-600 py-10 md:py-20">
            <p class="text-lg md:text-xl font-medium mb-3 md:mb-4 animate-pulse">Memuat produk dan kategori...</p>
            <div class="loader-lg mt-3 md:mt-4"></div>
          </div>
          <div v-else-if="productStore.error || categoriesDataError" class="text-center text-red-600 py-10 md:py-20">
            <Icon name="mdi:alert-circle" class="text-4xl md:text-5xl text-red-500 mb-2 md:mb-3" />
            <p class="text-lg md:text-xl font-medium mb-1 md:mb-2">Gagal memuat produk:</p>
            <p class="text-xs md:text-sm">{{ productStore.error?.message || categoriesDataError?.message || 'Terjadi kesalahan saat memuat data.' }}</p>
            <button @click="refreshAllEssentialData" class="mt-3 md:mt-4 bg-red-100 text-red-700 py-2 px-3 rounded-md hover:bg-red-200 transition duration-200 text-sm">
              Coba Lagi
            </button>
          </div>
          <div v-else-if="filteredProducts && filteredProducts.length === 0" class="text-center text-gray-500 py-10 md:py-20">
            <Icon name="mdi:magnify-remove-outline" class="text-4xl md:text-5xl text-gray-400 mb-2 md:mb-3" />
            <p class="text-lg md:text-xl font-medium">Produk Tidak Ditemukan</p>
            <p class="text-xs md:text-sm mt-0.5 md:mt-2">Coba sesuaikan filter atau kata kunci pencarian Anda.</p>
          </div>
          <div v-else>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-4 gap-4 md:gap-6 product-grid-area">
              <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" />
            </div>
            <div v-if="productStore.products.length > productDisplayLimit" class="mt-6 md:mt-8 text-center">
              <button
                @click="navigateToProductPage"
                class="px-6 py-2.5 md:px-8 md:py-3 bg-purple-600 text-white font-semibold rounded-lg shadow-md hover:bg-purple-700 transition duration-200 ease-in-out transform active:scale-95 flex items-center justify-center mx-auto gap-1 md:gap-2 text-sm md:text-base"
              >
                <Icon name="mdi:chevron-right-circle-outline" class="text-lg md:text-xl" /> Lihat daftar produk
              </button>
            </div>
          </div>
        </div>
      </div>

      
    </div>

    <!-- Modal untuk Barcode Scanner -->
    
  </div>
</template>

<script setup>
import { ref, computed, watch, provide, onMounted } from 'vue';
import { useProductStore } from '~/store/products';
import { useCartStore } from '~/store/cart';
import { useOrderStore } from '~/store/orders';
import { useApiClient } from '~/composables/useApiFetch'; 
import { useRouter } from 'vue-router'; 

// Import komponen


import ProductCard from '~/components/ProductCard.vue'; 


// --- Pinia Stores ---
const productStore = useProductStore();
const cartStore = useCartStore();
const orderStore = useOrderStore();
const router = useRouter(); 

// --- State Reaktif ---
const searchQuery = ref('');
const selectedCategory = ref('');
const selectedSubCategory = ref('');

const showLowStockAlert = ref(false);

const tanggalMulai = ref('');
const tanggalAkhir = ref('');

const dailySummary = ref({
  totalSales: 0,
  totalOrders: 0,
  dateRange: 'Hari Ini'
});

const productDisplayLimit = ref(4); 

const initializeDateRange = () => {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  tanggalMulai.value = `${yyyy}-${mm}-${dd}`;
  tanggalAkhir.value = `${yyyy}-${mm}-${dd}`;
};
initializeDateRange();

// --- Fungsi untuk memuat ulang Ringkasan Harian ---
const refreshDailySummary = async () => {
  const apiClient = useApiClient(); // Dapatkan instance di sini
  if (!tanggalMulai.value || !tanggalAkhir.value) {
    initializeDateRange();
  }

  let params = {
    start_date: tanggalMulai.value,
    end_date: tanggalAkhir.value,
  };
  let dateDisplay;
  if (tanggalMulai.value === tanggalAkhir.value) {
    dateDisplay = `Tanggal ${tanggalMulai.value}`;
  } else {
    dateDisplay = `${tanggalMulai.value} s/d ${tanggalAkhir.value}`;
  }

  try {
    const data = await apiClient('/orders/daily_summary/', { params });
    dailySummary.value = {
      totalSales: parseFloat(data.total_revenue) || 0,
      totalOrders: parseInt(data.total_transactions) || 0,
      dateRange: dateDisplay
    };
  } catch (error) {
    console.error("Error fetching daily summary:", error);
    dailySummary.value = { totalSales: 0, totalOrders: 0, dateRange: dateDisplay };
  }
};

// --- useAsyncData untuk Produk dan Kategori (Data yang diambil saat refresh/SSR) ---
const { pending: productsDataLoading, error: productsDataError } = useAsyncData(
  'initial-products',
  async () => {
    await productStore.fetchProducts({});
  },
  {
    server: true, 
    lazy: false,
  }
);

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

// --- Computed Property untuk Sub-Kategori yang Tersedia ---
const availableSubcategories = computed(() => {
  if (!productStore.categories || !selectedCategory.value) {
    return [];
  }
  return productStore.getSubcategoriesByCategoryId(selectedCategory.value);
});

// --- Watcher untuk Mereset Sub-Kategori saat Kategori Utama Berubah ---
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

const lowStockProducts = computed(() => {
  if (!productStore.products) {
    return [];
  }
  return productStore.products.filter(p => p.stock > 0 && p.stock < 10);
});

// PERUBAHAN UTAMA: Filter produk untuk tampilan terbatas
const filteredProducts = computed(() => { // Mengubah nama dari displayedProducts menjadi filteredProducts
  if (!productStore.products) {
    return [];
  }
  // Terapkan limit di sini jika Anda ingin membatasi tampilan utama
  // Jika Anda ingin semua produk yang difilter tampil, hapus .slice()
  return productStore.products.slice(0, productDisplayLimit.value);
});

// Fungsi untuk navigasi ke halaman produk penuh
const navigateToProductPage = () => {
  router.push('/products'); 
};


watch(lowStockProducts, (newValue) => {
  showLowStockAlert.value = newValue.length > 0;
}, { immediate: true });

// --- Fungsi Utama untuk merefresh SEMUA data esensial setelah transaksi ---
const refreshAllEssentialData = async () => {
  console.log('Refreshing all essential data after transaction...');
  await refreshDailySummary(); 
  await applyProductFilters(); 
  cartStore.clearCart();
  searchQuery.value = '';
  selectedCategory.value = '';
  selectedSubCategory.value = '';
};

// Menyediakan fungsi refreshAllEssentialData ke komponen anak (misal CheckoutForm)
provide('refreshData', refreshAllEssentialData);

// --- Hooks Lifecycle ---
onMounted(async () => {
  await refreshDailySummary();
});

// Watcher untuk memicu refreshAllEssentialData setelah keranjang kosong (indikasi checkout berhasil)
watch(() => cartStore.totalItems, async (newTotal, oldTotal) => {
  if (oldTotal > 0 && newTotal === 0) {
    console.log('Cart emptied, likely checkout. Refreshing data...');
    await refreshAllEssentialData();
  }
});


</script>

<style scoped>
/* Base Layout & Container */
.container {
  /* Hapus max-width eksplisit di sini jika sebelumnya ada, 
     biarkan mx-auto dan px- untuk responsivitas */
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
  height: 8px; /* Tambahkan tinggi untuk scrollbar horizontal */
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1; /* Warna abu-abu lembut */
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a0aec0; /* Warna abu-abu lebih gelap saat hover */
}

/* Loader Styling */
.loader-lg {
  border: 6px solid #e0e0e0;
  border-top: 6px solid #6366f1; /* Warna primer */
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

/* Animations */
@keyframes slide-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-slide-in-down {
  animation: slide-in-down 0.5s ease-out forwards;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}

/* Hover effects for cards */
.transform.hover\:scale-\[1\.005\]:hover {
    transform: scale(1.005);
}

/* Group hover for summary cards */
.group:hover .group-hover\:scale-110 {
    transform: scale(1.1);
}

/* ========================================================== */
/* Penyesuaian Ketinggian Daftar Produk di Desktop */
/* ========================================================== */
</style>
