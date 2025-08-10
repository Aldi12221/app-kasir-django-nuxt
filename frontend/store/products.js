// cashier_frontend/store/products.js
import { defineStore } from 'pinia';
import { useApiFetch } from '~/composables/useApiFetch'; // Import custom composable
import { useAuthStore } from './auth';

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    categories: [],
    loading: false,
    error: null,
  }),


  
  actions: {
    async addSubCategory(payload) {
      this.loading = true;
      this.error = null;
      try {
        // Hapus useRuntimeConfig dan logika manual baseUrl & headers di sini.
        // useApiFetch akan menangani otorisasi dan base URL secara otomatis.

        const { data: newSubCategory } = await useApiFetch('subcategories/', { // <--- GUNAKAN useApiFetch DI SINI
          method: 'POST',
          body: payload, // Payload sudah sesuai {name, category}
        });

        console.log('Sub-category added:', newSubCategory.value); // Akses data dengan .value
        await this.fetchCategories(); // Refresh kategori
        return true;
      } catch (error) {
        console.error('Error adding sub-category:', error);
        if (error.statusCode === 401) {
          this.error = 'Anda tidak memiliki izin untuk melakukan tindakan ini. Silakan login kembali.';
        } else {
          // Akses pesan error dari response data jika tersedia
          this.error = error.data?.detail || error.data?.message || 'Gagal menambahkan sub-kategori. Periksa koneksi atau input Anda.';
        }
        return false;
      } finally {
        this.loading = false;
      }
    },
    async fetchProducts(filters = {}) { // Ganti nama menjadi fetchProductsData agar tidak bentrok dengan nama di useAsyncData
      this.loading = true;
      this.error = null;
      try {
        const apiClient = useApiClient();
        // PASTIKAN BARIS INI BENAR: Meneruskan filters sebagai paramsz
        const response = await apiClient('/products', { params: filters });
        this.products = response;
      } catch (error) {
        this.error = error;
        console.error('Error fetching products:', error);
      } finally {
        this.loading = false;
      }
    },
    async fetchCategories() {
      this.loading = true;
      this.error = null;
      try {
        const apiClient = useApiClient();
        const response = await apiClient('/categories');
        
        // --- PERBAIKAN KRITIS DI SINI ---
        // Memastikan `response` adalah array dan setiap elemen adalah objek valid dengan 'id'
        if (Array.isArray(response)) {
          this.categories = response.filter(cat => cat && typeof cat === 'object' && 'id' in cat);
        } else {
          // Fallback jika API tidak mengembalikan array (misalnya, objek data)
          // Anda mungkin perlu menyesuaikan ini jika struktur respons API berbeda
          console.warn('API /categories expected to return an array, but received:', response);
          this.categories = []; // Atur ke array kosong untuk mencegah error
        }
        
      } catch (error) {
        this.error = error;
        console.error('Error fetching categories and subcategories:', error);
      } finally {
        this.loading = false;
      }
    },
  
    async addProduct(productData) {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await useApiFetch('/products/', { // Gunakan useApiFetch
          method: 'POST',
          body: productData,
        });
        this.products.push(data.value);
        return true;
      } catch (e) {
        this.error = e;
        console.error("Error adding product:", e);
        return false;
      } finally {
        this.loading = false;
      }
    },
    // Tambahkan aksi lain seperti updateProduct, deleteProduct, dll., menggunakan useApiFetch
    async updateProduct(id, productData) {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await useApiFetch(`/products/${id}/`, {
          method: 'PUT', // Atau PATCH
          body: productData,
        });
        const index = this.products.findIndex(p => p.id === id);
        if (index !== -1) {
          this.products[index] = data.value;
        }
        return true;
      } catch (e) {
        this.error = e;
        console.error("Error updating product:", e);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async deleteProduct(id) {
      this.loading = true;
      this.error = null;
      try {
        await useApiFetch(`/products/${id}/`, {
          method: 'DELETE',
        });
        this.products = this.products.filter(p => p.id !== id);
        return true;
      } catch (e) {
        this.error = e;
        console.error("Error deleting product:", e);
        return false;
      } finally {
        this.loading = false;
      }
    },
    async addCategory(category) {
        this.loading = true;
        this.error = null;
        try {
          // Kirim permintaan POST ke API untuk menambah kategori baru
          const { data: newCategory } = await useApiFetch('/categories/', {
            method: 'POST',
            body: { name: category }, // Sesuaikan dengan field nama kategori di backend Anda
          });
  
          if (newCategory.value) {  
            this.categories.push(newCategory.value); // Tambahkan kategori baru ke state
            return true; // Berhasil
          }
          return false; // Gagal
        } catch (e) {
          console.error('Error adding category:', e);
          this.error = e.response?._data?.detail || 'Gagal menambahkan kategori.';
          return false; // Gagal
        } finally {
          this.loading = false;
        }
      },
  },
  getters: {
  // Getter ini adalah kunci untuk mendapatkan sub-kategori yang relevan
  getSubcategoriesByCategoryId: (state) => (categoryId) => {
    if (!categoryId) {
      return []; // Jika tidak ada categoryId yang dipilih, kembalikan array kosong
    }
    // Mencari objek kategori utama berdasarkan categoryId
    const category = state.categories.find(cat => cat.id == categoryId);
    // Mengembalikan array subcategories dari objek kategori yang ditemukan
    // Jika kategori tidak ditemukan atau tidak memiliki subcategories, kembalikan array kosong
    return category && category.subcategories ? category.subcategories : [];
  },
},

   persist: true
   

});