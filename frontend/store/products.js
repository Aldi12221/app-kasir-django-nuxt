// cashier_frontend/store/products.js
import { defineStore } from 'pinia';
import { useApiFetch } from '~/composables/useApiFetch'; // Import custom composable

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    categories: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchProducts() { // Ganti nama menjadi fetchProductsData agar tidak bentrok dengan nama di useAsyncData
      this.loading = true;
      this.error = null;
      try {
        const apiClient = useApiClient();
        const response = await apiClient('/products/');
        this.products = response; 
      } catch (error) {
        this.error = error;
        console.error('Error fetching products:', error);
      } finally {
        this.loading = false;
      }
    },
    async fetchCategories() { // Ganti nama menjadi fetchCategoriesData
      this.loading = true; 
      this.error = null;
      try {
        const apiClient = useApiClient();
        const response = await apiClient('/categories/'); 
        this.categories = response; 
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
    getSubcategoriesByCategoryId: (state) => (categoryId) => {
      if (!categoryId) return [];
      const category = state.categories.find(cat => cat.id == categoryId);
      return category && category.subcategories ? category.subcategories : [];
    },
  },

   persist: true
   

});