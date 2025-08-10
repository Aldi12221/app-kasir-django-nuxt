<template>
  <div class="p-4 border rounded-lg shadow-md">
    <h3 class="text-xl font-bold mb-4">Total Belanja: Rp {{ (cartStore.totalAmount ?? 0).toLocaleString('id-ID') }}</h3>
    <div class="mb-4">
      <label for="paymentMethod" class="block text-gray-700 text-sm font-bold mb-2">Metode Pembayaran:</label>
      <select v-model="paymentMethod" id="paymentMethod" class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        <option value="cash">Tunai</option>
        <option value="card">Kartu Debit/Kredit</option>
        <option value="qr">QRIS</option>
      </select>
    </div>
    <button
      @click="processCheckout"
      :disabled="cartStore.totalItems === 0 || processing"
      class="bg-green-500 text-white py-2 px-4 rounded w-full hover:bg-green-600 disabled:bg-gray-400"
    >
      {{ processing ? 'Memproses...' : 'Bayar Sekarang' }}
    </button>
    <p v-if="checkoutError" class="text-red-500 text-sm mt-2">{{ checkoutError }}</p>
    <p v-if="checkoutSuccess" class="text-green-500 text-sm mt-2">Pembayaran Berhasil! ID Pesanan: {{ checkoutSuccess }}</p>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import { useCartStore } from '~/store/cart';
import { useOrderStore } from '~/store/orders';

const cartStore = useCartStore();
const orderStore = useOrderStore();

const paymentMethod = ref('cash');
const processing = ref(false);
const checkoutError = ref(null);
const checkoutSuccess = ref(null);

const refreshData = inject('refreshData');

const processCheckout = async () => {
  processing.value = true;
  checkoutError.value = null; // Reset error message
  checkoutSuccess.value = null; // Reset success message

  try {
    const orderData = {
      total_amount: cartStore.totalAmount,
      payment_method: paymentMethod.value,
      items: cartStore.items.map(item => ({
        product: item.id,
        quantity: item.quantity,
        price_at_purchase: item.price,
      })),
    };

    const newOrder = await orderStore.addOrder(orderData); // Memanggil Pinia action

    // --- Perubahan Penanganan Respons di Sini ---
    if (newOrder && newOrder.id) { // Jika newOrder adalah objek dan memiliki ID
      checkoutSuccess.value = newOrder.id;
      cartStore.clearCart();
      if (refreshData) {
        refreshData(); // Pemicu hard refresh
      }
    } else {
      // Jika newOrder adalah null (karena ada error di store)
      // Gunakan error dari store, atau pesan default jika tidak ada
      checkoutError.value = orderStore.error?.message || 'Terjadi kesalahan saat memproses pembayaran.';
      console.warn("Checkout failed or response invalid:", orderStore.error);
    }

  } catch (error) {
    // Ini akan menangkap error yang benar-benar dilempar dari `addOrder` atau `useApiFetch`
    checkoutError.value = error.message || 'Terjadi kesalahan tidak terduga saat memproses pembayaran.';
    console.error("Error during checkout process:", error);
  } finally {
    processing.value = false;
  }
};
</script>