<template>
  <div class="product-detail-page p-4 md:p-8 bg-gray-50 min-h-screen">
    <h1 class="text-2xl md:text-3xl font-bold mb-4 text-gray-800">Detail & Edit Produk</h1>

    <div v-if="productStore.loading" class="text-center text-gray-600 py-10">
      <p class="text-lg mb-2">Memuat detail produk...</p>
      <div class="loader-lg"></div>
    </div>
    <div v-else-if="productStore.error" class="text-center text-red-600 py-10">
      <Icon name="mdi:alert-circle" class="text-red-500 text-5xl mb-3" />
      <p class="text-xl font-medium mb-2">Gagal memuat produk:</p>
      <p class="text-sm">{{ productStore.error.message || 'Terjadi kesalahan saat memuat data.' }}</p>
    </div>
    <div v-else-if="!product" class="text-center text-gray-600 py-10">
      <Icon name="mdi:alert-box-outline" class="text-gray-400 text-5xl mb-3" />
      <p class="text-lg">Produk tidak ditemukan.</p>
    </div>
    <div v-else class="p-6 bg-white rounded-lg shadow-xl border border-gray-200">
      <form @submit.prevent="updateExistingProduct">
        <div class="mb-4">
          <label for="productName" class="block text-sm font-semibold text-gray-700 mb-1">Nama Produk</label>
          <input type="text" id="productName" v-model="product.name" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-base" required>
        </div>

        <div class="mb-4">
          <label for="productDesc" class="block text-sm font-semibold text-gray-700 mb-1">Deskripsi</label>
          <textarea id="productDesc" v-model="product.description" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-base"></textarea>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label for="productPrice" class="block text-sm font-semibold text-gray-700 mb-1">Harga (Rp)</label>
            <input type="number" id="productPrice" v-model="product.price" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-base" step="0.01" required>
          </div>
          <div>
            <label for="productStock" class="block text-sm font-semibold text-gray-700 mb-1">Stok</label>
            <input type="number" id="productStock" v-model="product.stock" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-base" required>
          </div>
          <div>
            <label for="productStock" class="block text-sm font-semibold text-gray-700 mb-1">barcode</label>
            <input type="number" id="productStock" v-model="product.barcode" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-base" required>
          </div>
        </div>

        <div class="mb-4">
          <label for="productCategory" class="block text-sm font-semibold text-gray-700 mb-1">Kategori</label>
          <select id="productCategory" v-model="product.category" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-base">
            <option :value="null">-- Pilih Kategori --</option>
            <option v-for="cat in productStore.categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <div v-if="availableSubcategories.length > 0" class="mb-4">
          <label for="productSubCategory" class="block text-sm font-semibold text-gray-700 mb-1">Subkategori</label>
          <select id="productSubCategory" v-model="product.sub_category" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-base">
            <option :value="null">-- Pilih Subkategori --</option>
            <option v-for="subcat in availableSubcategories" :key="subcat.id" :value="subcat.id">
              {{ subcat.name }}
            </option>
          </select>
        </div>
        <div v-else-if="product.category && !productStore.loadingCategories" class="mb-4 text-sm text-gray-500">
          Tidak ada subkategori tersedia untuk kategori ini.
        </div>


        <div class="mb-6">
          <label for="productImage" class="block text-sm font-semibold text-gray-700 mb-1">Gambar Produk</label>
          <input type="file" id="productImage" @change="handleExistingImageUpload" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100">
          
          <div v-if="imagePreview || product.image" class="mt-4 flex items-center gap-4">
            <img :src="product.image" alt="Current Image" class="w-24 h-24 md:w-32 md:h-32 object-cover rounded-lg shadow-sm border border-gray-200">
            <button v-if="imagePreview || product.image" @click="clearImage" type="button" class="text-red-600 hover:text-red-800 text-sm flex items-center gap-1">
                <Icon name="mdi:close-circle" class="text-lg" /> Hapus Gambar
            </button>
          </div>
          <p v-else class="text-gray-500 text-sm mt-2">Belum ada gambar produk.</p>
        </div>

        <div class="flex items-center gap-3">
            <button type="submit" class="px-6 py-2 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-200" :disabled="productStore.loading">
              <span v-if="productStore.loading" class="flex items-center gap-2">
                <div class="spinner"></div> Menyimpan...
              </span>
              <span v-else>
                <Icon name="mdi:content-save-outline" class="mr-2" />Simpan Perubahan
              </span>
            </button>
            <button type="button" @click="confirmDeleteProduct" class="px-6 py-2 bg-red-600 text-white font-semibold rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-200" :disabled="productStore.loading">
              <Icon name="mdi:delete-outline" class="mr-2" />Hapus Produk
            </button>
            <NuxtLink :to="`/products`" class="px-3 py-1 bg-gray-500 text-white rounded-md hover:bg-yellow-600 mr-2">Back</NuxtLink>
        </div>

        <p v-if="productStore.error" class="text-red-500 mt-4 text-sm">{{ productStore.error.message }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // Impor useRouter
import { useProductStore } from '@/store/products';

const productStore = useProductStore();
const route = useRoute();
const router = useRouter(); // Inisialisasi useRouter
const runtimeConfig = useRuntimeConfig();

const productId = computed(() => route.params.id);
const product = ref(null); // Akan menampung data produk yang akan diedit
const newImageFile = ref(null); // Akan menampung file gambar baru yang diupload
const imagePreview = ref(null); // Untuk preview gambar baru
const shouldRemoveImage = ref(false); // Flag untuk menandakan gambar harus dihapus

// Fungsi untuk mendapatkan URL gambar yang lengkap
const productImageUrl = (relativePath) => {
    if (relativePath) {
        // Asumsi base URL untuk media ada di runtimeConfig.public.mediaBaseUrl
        // Atau jika hanya ada apiBaseUrl, sesuaikan path-nya
        return `${runtimeConfig.public.mediaBaseUrl || runtimeConfig.public.apiBaseUrl}${relativePath}`;
    }
    return ''; // Atau URL placeholder
};

// Computed property untuk subkategori yang tersedia berdasarkan kategori yang dipilih
const availableSubcategories = computed(() => {
  if (!productStore.categories || !product.value || !product.value.category) {
    return [];
  }
  return productStore.getSubcategoriesByCategoryId(product.value.category);
});

// Watcher untuk mereset sub-kategori saat kategori utama berubah
watch(() => product.value?.category, (newCategoryId, oldCategoryId) => {
  if (newCategoryId !== oldCategoryId) {
    // Hanya reset jika sub_category yang saat ini dipilih tidak ada di subkategori yang baru tersedia
    // Ini mencegah reset jika user mengganti kategori dan kemudian kembali ke kategori sebelumnya
    const currentSubCategoryId = product.value?.sub_category;
    const isCurrentSubCategoryAvailable = availableSubcategories.value.some(subcat => subcat.id === currentSubCategoryId);

    if (!isCurrentSubCategoryAvailable) {
      product.value.sub_category = null;
    }
  }
});

// Mengambil data produk berdasarkan ID
const fetchProductDetails = async () => {
    await productStore.fetchCategories(); // Pastikan kategori dan subkategori dimuat
    await productStore.fetchProducts(); // Pastikan daftar produk sudah ada

    const foundProduct = productStore.products.find(p => p.id == productId.value);
    if (foundProduct) {
        // Deep copy untuk menghindari mutasi langsung pada store state
        product.value = JSON.parse(JSON.stringify(foundProduct));
        
        // Pastikan category dan sub_category diubah ke ID jika masih objek
        if (product.value.category && typeof product.value.category === 'object') {
            product.value.category = product.value.category.id;
        }
        if (product.value.sub_category && typeof product.value.sub_category === 'object') {
            product.value.sub_category = product.value.sub_category.id;
        }
        
        // Atur imagePreview jika ada gambar produk
        if (product.value.image) {
            imagePreview.value = productImageUrl(product.value.image); // Gunakan URL lengkap untuk preview
        }
    } else {
        console.warn(`Product with ID ${productId.value} not found.`);
        // Opsional: Redirect ke halaman daftar produk atau 404
        router.push('/products'); 
    }
};

// Handle upload gambar untuk produk yang sudah ada
const handleExistingImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        newImageFile.value = file;
        shouldRemoveImage.value = false; // Jika ada gambar baru, batalkan penghapusan
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        newImageFile.value = null;
        // Tidak perlu mereset imagePreview di sini, biarkan gambar lama tampil
        // sampai user mengklik 'Hapus Gambar' secara eksplisit
    }
};

// Fungsi untuk menghapus gambar yang ada atau preview gambar baru
const clearImage = () => {
    newImageFile.value = null; // Hapus file yang baru diupload
    imagePreview.value = null; // Hapus preview
    shouldRemoveImage.value = true; // Tandai untuk dihapus di backend
    product.value.image = null; // Secara visual hapus gambar dari model
};


// Mengupdate produk yang sudah ada
const updateExistingProduct = async () => {
    const formData = new FormData();
    formData.append('name', product.value.name);
    formData.append('description', product.value.description || ''); // Pastikan tidak null
    formData.append('price', product.value.price);
    formData.append('stock', product.value.stock);
    formData.append('barcode', product.value.barcode);
    
    // Kategori
    if (product.value.category) {
        formData.append('category', product.value.category);
    } else {
        formData.append('category', ''); // Kirim string kosong jika null untuk backend Django
    }

    // Subkategori
    if (product.value.sub_category) {
        formData.append('sub_category', product.value.sub_category);
    } else {
        formData.append('sub_category', ''); // Kirim string kosong jika null
    }

    // Penanganan Gambar
    if (newImageFile.value) {
        // Jika ada file baru yang dipilih, kirim file tersebut
        formData.append('image', newImageFile.value);
    } else if (shouldRemoveImage.value) {
        // Jika user mengklik "Hapus Gambar", kirim string kosong untuk menghapus gambar di backend
        formData.append('image', '');
    }
    // Jika tidak ada file baru dan tidak ada penghapusan, biarkan field 'image' tidak dikirim
    // sehingga backend akan mempertahankan gambar yang ada.

    try {
        await productStore.updateProduct(productId.value, formData);
        alert('Produk berhasil diperbarui!');
        // Setelah berhasil update, refresh detail produk untuk menampilkan data terbaru (termasuk gambar)
        await fetchProductDetails();
        // Reset state upload gambar
        newImageFile.value = null;
        shouldRemoveImage.value = false;
        // Opsional: navigasi kembali ke daftar produk atau tampilkan pesan sukses
        // router.push('/products'); 
    } catch (error) {
        console.error("Error updating product:", error);
        alert(`Gagal memperbarui produk: ${error.message || 'Terjadi kesalahan'}`);
    }
};

const confirmDeleteProduct = async () => {
  if (confirm('Apakah Anda yakin ingin menghapus produk ini? Tindakan ini tidak dapat dibatalkan.')) {
    try {
      await productStore.deleteProduct(productId.value);
      alert('Produk berhasil dihapus!');
      router.push('/products'); // Redirect ke halaman daftar produk setelah dihapus
    } catch (error) {
      console.error("Error deleting product:", error);
      alert(`Gagal menghapus produk: ${error.message || 'Terjadi kesalahan'}`);
    }
  }
};


onMounted(async () => {
  await fetchProductDetails(); // Ambil detail produk dan kategori saat komponen dimuat
});
</script>

<style scoped>
.product-detail-page {
  max-width: 900px;
  margin: 0 auto;
}

.loader-lg {
  border: 6px solid #e0e0e0; /* Smaller border for mobile */
  border-top: 6px solid #8B5CF6; /* Purple-500 */
  width: 60px; /* Smaller width for mobile */
  height: 60px; /* Smaller height for mobile */
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Spinner untuk tombol */
.spinner {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid #fff;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}
</style>