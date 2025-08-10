// ~/store/orders.js
import { defineStore } from 'pinia';
import { useApiFetch } from '~/composables/useApiFetch'; // Pastikan path ini benar

export const useOrderStore = defineStore('orders', {
  state: () => ({
    orders: [],
    loading: false,
    error: null,
  }),
  actions: {
    async addOrder(orderData) {
      this.loading = true;
      this.error = null; // Pastikan error di-reset
      try {
        // --- PERUBAHAN UTAMA DI SINI: Ambil 'error' juga dari useApiFetch ---
        const { data, error } = await useApiFetch('/orders/process_checkout/', {
          method: 'POST',
          body: orderData,
        });

        // --- Cek apakah ada error dari useApiFetch ---
        if (error.value) {
          // Jika ada error dari API (misal 4xx, 5xx), tangkap dan set this.error
          this.error = error.value; // Set error object secara langsung
          console.error("API Error adding order:", error.value);
          // throw error.value; // PENTING: Lempar error agar ditangkap oleh try/catch di komponen
          // ATAU, jika Anda ingin mengelola error di store dan mengembalikan null/false:
          return null; // Mengembalikan null untuk menandakan kegagalan eksplisit
        }

        // Jika tidak ada error dan data berhasil diterima
        if (data.value) {
          this.orders.push(data.value);
          // Mengembalikan data pesanan yang berhasil (bukan hanya true)
          // Agar komponen bisa mengakses ID pesanan
          return data.value;
        } else {
          // Kasus aneh jika tidak ada error tapi juga tidak ada data
          this.error = new Error("Respons API tidak memiliki data valid.");
          console.error("No data received for order:", data.value);
          return null;
        }
      } catch (e) {
        // Ini menangkap error jaringan atau error lain yang benar-benar dilempar
        this.error = e;
        console.error("Unexpected error during add order:", e);
        return null; // Mengembalikan null untuk menandakan kegagalan
      } finally {
        this.loading = false;
      }
    },
    // Anda mungkin juga i
    async fetchOrders() {
      this.loading = true;
      this.error = null;
      try {
        const { data, error } = await useApiFetch('/orders/');
        if (error.value) {
          throw new Error(error.value.message || 'Gagal memuat transaksi.');
        }
        this.orders = data.value || [];
      } catch (e) {
        this.error = e;
        console.error('Error fetching orders:', e);
      } finally {
        this.loading = false;
      }
    },

    async updateOrder(id, payload) {
      this.loading = true;
      this.error = null;
      try {
        const { data, error } = await useApiFetch(`/orders/${id}/`, {
          method: 'PATCH', // Gunakan PATCH untuk update sebagian
          body: payload,
        });
        if (error.value) {
          throw new Error(error.value.message || 'Gagal memperbarui transaksi.');
        }
        // Perbarui transaksi di state lokal
        const index = this.orders.findIndex(order => order.id === id);
        if (index !== -1) {
          this.orders[index] = { ...this.orders[index], ...data.value };
        }
        return true;
      } catch (e) {
        this.error = e;
        console.error('Error updating order:', e);
        return false;
      } finally {
        this.loading = false;
      }
    },

    // PASTIKAN FUNGSI deleteOrder INI ADA DAN TIDAK ADA TYPO
    async deleteOrder(id) {
      this.loading = true;
      this.error = null;
      try {
        const { error } = await useApiFetch(`/orders/${id}/`, {
          method: 'DELETE',
        });
        if (error.value) {
          throw new Error(error.value.message || 'Gagal menghapus transaksi.');
        }
        // Hapus transaksi dari state lokal
        this.orders = this.orders.filter(order => order.id !== id);
        return true;
      } catch (e) {
        this.error = e;
        console.error('Error deleting order:', e);
        return false;
      } finally {
        this.loading = false;
      }
    },
  },
});