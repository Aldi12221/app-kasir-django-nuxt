<template>
  <div class="container mx-auto p-4 flex flex-col lg:flex-row gap-6">
    <div class="flex-1 flex flex-col gap-6">
      <div v-if="showLowStockAlert" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded-md shadow-md" role="alert">
        <p class="font-bold">Peringatan Stok Rendah!</p>
        <p class="text-sm">Beberapa produk memiliki stok kurang dari 10. Segera lakukan restock:</p>
        <ul class="list-disc list-inside text-sm mt-2">
          <li v-for="product in lowStockProducts" :key="product.id">
            {{ product.name }} (Stok: {{ product.stock }})
          </li>
        </ul>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-bold mb-4">Ringkasan Penjualan <span class="text-blue-600">({{ dailySummary.dateRange }})</span></h2>

        <div class="flex flex-col md:flex-row gap-4 mb-4 items-center">
          <div>
            <label for="tanggalMulai" class="block text-sm font-medium text-gray-700">Tanggal Mulai:</label>
            <input
              type="date"
              id="tanggalMulai"
              v-model="tanggalMulai"
              class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            >
          </div>
          <div>
            <label for="tanggalAkhir" class="block text-sm font-medium text-gray-700">Tanggal Akhir:</label>
            <input
              type="date"
              id="tanggalAkhir"
              v-model="tanggalAkhir"
              class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            >
          </div>
          <button
            @click="refreshDailySummary"
            class="mt-4 md:mt-0 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline self-end"
          >
            Tampilkan
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-5 rounded-lg shadow-md flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-500">Total Penjualan</h3>
              <p class="text-3xl font-bold text-green-600">Rp {{ dailySummary.totalSales.toLocaleString('id-ID') }}</p>
            </div>
            <Icon name="mdi:cash-multiple" class="text-green-600 text-4xl" />
          </div>
          <div class="bg-white p-5 rounded-lg shadow-md flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-500">Total Transaksi</h3>
              <p class="text-3xl font-bold text-blue-600">{{ dailySummary.totalOrders }}</p>
            </div>
            <Icon name="mdi:receipt-text-outline" class="text-blue-600 text-4xl" />
          </div>
          <div class="bg-white p-5 rounded-lg shadow-md flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-500">Produk Stok Rendah</h3>
              <p class="text-3xl font-bold text-orange-600">{{ lowStockProducts.length }}</p>
            </div>
            <Icon name="mdi:alert-circle-outline" class="text-orange-600 text-4xl" />
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex flex-col md:flex-row justify-between items-center mb-4 gap-4">
          <h2 class="text-xl font-bold text-center md:text-left w-full md:w-auto">Daftar Produk</h2>

          <div class="flex flex-col sm:flex-row items-center gap-2 w-full md:w-auto">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Cari produk..."
              class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-full"
            />
            <select
              v-model="selectedCategory"
              class="shadow border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-full sm:w-auto"
            >
              <option value="">Semua Kategori</option>
              <option v-for="category in productStore.categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>

            <select
              v-model="selectedSubCategory"
              v-if="availableSubcategories.length > 0"
              class="shadow border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-full sm:w-auto"
            >
              <option value="">Semua Sub-Kategori</option>
              <option v-for="subcat in availableSubcategories" :key="subcat.id" :value="subcat.id">
                {{ subcat.name }}
              </option>
            </select>
          </div>
        </div>

        <div v-if="productStore.loading || productsDataLoading || categoriesDataLoading" class="text-center text-gray-500 py-10">
          <p>Memuat produk...</p>
          <div class="loader mt-4"></div>
        </div>
        <div v-else-if="productStore.error || productsDataError || categoriesDataError" class="text-center text-red-500 py-10">
          <p>Gagal memuat produk: {{ productStore.error?.message || productsDataError?.message || categoriesDataError?.message || 'Terjadi kesalahan saat memuat data.' }}</p>
          <p class="text-sm">Coba refresh halaman atau periksa koneksi Anda.</p>
        </div>
        <div v-else-if="filteredProducts && filteredProducts.length === 0" class="text-center text-gray-500 py-10">
          <p>Tidak ada produk yang ditemukan.</p>
        </div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" />
        </div>
      </div>
    </div>

    <div class="lg:w-1/3 bg-white p-6 rounded-lg shadow-md lg:sticky lg:top-4 h-fit">
      <h2 class="text-xl font-bold mb-4">Keranjang Belanja ({{ cartStore.totalItems || 0 }} item)</h2>
      <div v-if="!cartStore.items || cartStore.items.length === 0" class="text-gray-500 text-center py-6">Keranjang kosong.</div>
      <div v-else class="divide-y divide-gray-200 max-h-96 overflow-y-auto mb-4">
        <CartItem v-for="item in cartStore.items" :key="item.id" :item="item" />
      </div>
      <CheckoutForm class="mt-6" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, provide, onMounted } from 'vue';
import { useProductStore } from '~/store/products';
import { useCartStore } from '~/store/cart';
import { useOrderStore } from '~/store/orders';
import { useApiClient } from '~/composables/useApiFetch';

// --- Pinia Stores ---
const productStore = useProductStore();
const cartStore = useCartStore();
const orderStore = useOrderStore();

// --- State Reaktif ---
const searchQuery = ref('');
const selectedCategory = ref(''); // ID kategori utama yang dipilih
const selectedSubCategory = ref(''); // ID sub-kategori yang dipilih
const showLowStockAlert = ref(false);

const tanggalMulai = ref('');
const tanggalAkhir = ref('');

const dailySummary = ref({
  totalSales: 0,
  totalOrders: 0,
  dateRange: 'Hari Ini'
});

const initializeDateRange = () => {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  tanggalMulai.value = `${yyyy}-${mm}-${dd}`;
  tanggalAkhir.value = `${yyyy}-${mm}-${dd}`;
};
initializeDateRange();

// --- useAsyncData untuk Produk dan Kategori (Data yang diambil saat refresh/SSR) ---
const { pending: productsDataLoading, error: productsDataError } = useAsyncData(
  'initial-products',
  async () => {
    await productStore.fetchProductsData();
  },
  {
    server: true,
    lazy: false,
  }
);

const { pending: categoriesDataLoading, error: categoriesDataError } = useAsyncData(
  'initial-categories',
  async () => {
    await productStore.fetchCategoriesAndSubcategories();
  },
  {
    server: true,
    lazy: false,
  }
);

// --- Computed Property untuk Sub-Kategori yang Tersedia ---
const availableSubcategories = computed(() => {
  return productStore.getSubcategoriesByCategoryId(selectedCategory.value);
});

// --- Watcher untuk Mereset Sub-Kategori saat Kategori Utama Berubah ---
watch(selectedCategory, (newCategoryId) => {
  selectedSubCategory.value = ''; // Reset sub-kategori saat kategori utama berubah
  applyProductFilters(); // Panggil fungsi filter produk
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
    filters.category = parseInt(selectedCategory.value); // Pastikan ini ID kategori utama
  }
  if (selectedSubCategory.value) {
    filters.sub_category = parseInt(selectedSubCategory.value); // Pastikan ini ID sub-kategori
  }
  if (searchQuery.value) {
    filters.search = searchQuery.value;
  }
  await productStore.fetchProductsData(filters);
};

// --- Fungsi untuk Memuat Ulang Ringkasan Harian ---
const refreshDailySummary = async () => {
  const apiClient = useApiClient();

  if (!tanggalMulai.value || !tanggalAkhir.value) {
    initializeDateRange();
  }

  let params = {
    start_date: tanggalMulai.value,
    end_date: tanggalAkhir.value,
  };
  let dateDisplay = `${tanggalMulai.value} s/d ${tanggalAkhir.value}`;

  dailySummary.value.dateRange = dateDisplay;

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

onMounted(async () => {
  await refreshDailySummary();
});

// --- Computed Properties ---
const lowStockProducts = computed(() => {
  if (!productStore.products) {
    return [];
  }
  return productStore.products.filter(p => p.stock > 0 && p.stock < 10);
});

const filteredProducts = computed(() => {
  return productStore.products || [];
});

watch(lowStockProducts, (newValue) => {
  showLowStockAlert.value = newValue.length > 0;
}, { immediate: true });

watch(() => cartStore.totalItems, async (newTotal, oldTotal) => {
  if (oldTotal > 0 && newTotal === 0) {
    console.log('Cart emptied, likely checkout. Refreshing data...');
    await refreshAllEssentialData();
  }
});
</script>

<style scoped>
/* Contoh loader sederhana */
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 2s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>