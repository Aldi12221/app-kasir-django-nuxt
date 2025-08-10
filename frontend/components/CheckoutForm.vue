<template>
  <div class="checkout-form-card">
    <h3 class="text-2xl font-bold text-gray-800 mb-5 flex items-center gap-3">
      <Icon name="mdi:cash-fast" class="text-purple-600 text-3xl" />
      Pembayaran
    </h3>

    <div class="mb-6 bg-blue-50 p-4 rounded-lg flex items-center justify-between shadow-sm border border-blue-100 animate-fade-in-up">
      <p class="text-lg font-semibold text-blue-800">Total Belanja:</p>
      <p class="text-3xl font-extrabold text-blue-900">Rp {{ (cartStore.totalAmount ?? 0).toLocaleString('id-ID') }}</p>
    </div>

    <div class="mb-6">
      <label for="paymentMethod" class="block text-gray-700 text-sm font-semibold mb-2">Pilih Metode Pembayaran:</label>
      <div class="relative">
        <select 
          v-model="paymentMethod" 
          id="paymentMethod" 
          class="block appearance-none w-full bg-white border border-gray-300 text-gray-700 py-3 px-4 pr-8 rounded-lg shadow-sm leading-tight focus:outline-none focus:border-blue-500 focus:ring-blue-500 transition duration-200"
        >
          <option value="cash">Tunai</option>
          <option value="card">Kartu Debit/Kredit</option>
          <option value="qr">QRIS</option>
        </select>
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
          <Icon name="mdi:chevron-down" class="w-5 h-5" />
        </div>
      </div>
    </div>

    <Transition name="slide-fade">
      <div v-if="paymentMethod === 'cash'" class="mb-6">
        <label for="cashAmount" class="block text-gray-700 text-sm font-semibold mb-2">Nominal Tunai:</label>
        <input
          type="number"
          id="cashAmount"
          v-model.number="cashAmount"
          @input="calculateChange"
          placeholder="Masukkan nominal bayar..."
          class="w-full px-4 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 text-lg"
          min="0"
        />
        <p v-if="change < 0 && cashAmount > 0" class="text-red-500 text-sm mt-1">Pembayaran kurang Rp {{ (-change).toLocaleString('id-ID') }}</p>
        <p v-else-if="change >= 0" class="text-green-600 text-sm mt-1">Kembali: Rp {{ change.toLocaleString('id-ID') }}</p>
      </div>
    </Transition>

    <button
      @click="processCheckout"
      :disabled="!isFormValid || processing"
      class="w-full py-3.5 px-4 rounded-lg font-bold text-xl transition-all duration-300 ease-in-out 
             flex items-center justify-center gap-3 shadow-lg transform active:scale-98"
      :class="{
        'bg-green-600 text-white hover:bg-green-700': isFormValid && !processing,
        'bg-gray-400 text-gray-700 cursor-not-allowed': !isFormValid || processing,
      }"
    >
      <template v-if="processing">
        <Icon name="mdi:loading" class="animate-spin text-2xl" /> Memproses...
      </template>
      <template v-else>
        <Icon name="mdi:currency-usd" class="text-2xl" /> Bayar Sekarang
      </template>
    </button>

    <transition name="fade">
      <div v-if="checkoutError" class="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative flex items-center gap-2 animate-fade-in">
        <Icon name="mdi:alert-circle" class="text-red-500 text-2xl" />
        <div>
          <strong class="font-bold">Gagal!</strong>
          <span class="block sm:inline ml-1">{{ checkoutError }}</span>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="checkoutSuccess" class="mt-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg relative flex items-center gap-2 animate-fade-in">
        <Icon name="mdi:check-circle" class="text-green-500 text-2xl" />
        <div>
          <strong class="font-bold">Berhasil!</strong>
          <span class="block sm:inline ml-1">Pembayaran Selesai. ID Pesanan: <strong>{{ checkoutSuccess }}</strong></span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, inject, computed } from 'vue'; // Import computed
import { useCartStore } from '~/store/cart';
import { useOrderStore } from '~/store/orders';

const cartStore = useCartStore();
const orderStore = useOrderStore();

// State Form
const paymentMethod = ref('cash');
const cashAmount = ref(0); // Tambahkan state untuk nominal tunai
const processing = ref(false);
const checkoutError = ref(null);
const checkoutSuccess = ref(null);

const refreshData = inject('refreshData'); // Injeksi fungsi refresh dari parent

// Computed: Perhitungan Kembalian
const change = computed(() => {
  return cashAmount.value - (cartStore.totalAmount ?? 0);
});

// Computed: Validasi Form
const isFormValid = computed(() => {
  if ((cartStore.totalAmount ?? 0) === 0 || cartStore.totalItems === 0) {
    return false; // Keranjang kosong, tidak bisa checkout
  }
  if (paymentMethod.value === 'cash') {
    return cashAmount.value >= (cartStore.totalAmount ?? 0);
  }
  return true; // Untuk metode pembayaran lain, anggap valid
});

const calculateChange = () => {
  // Fungsi ini otomatis dipanggil oleh v-model.number dan @input
  // Tidak perlu logika tambahan di sini karena `change` sudah computed
};

const processCheckout = async () => {
  if (!isFormValid.value || processing.value) { // Gunakan isFormValid
    checkoutError.value = "Keranjang kosong atau pembayaran belum memenuhi syarat.";
    // Hilangkan pesan error setelah beberapa saat
    setTimeout(() => {
      checkoutError.value = null;
    }, 3000); 
    return;
  }

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
        // Gunakan `price_at_order` sesuai skema DB sebelumnya
      })),
      // Anda bisa tambahkan field lain seperti `notes` jika ada di model order Anda
    };

    const newOrder = await orderStore.addOrder(orderData);

    if (newOrder && newOrder.id) {
      checkoutSuccess.value = newOrder.id;
      // Beri sedikit jeda agar user bisa melihat pesan sukses
      setTimeout(async () => {
        cartStore.clearCart();
        if (refreshData) {
          await refreshData(); // Panggil fungsi refresh dari parent untuk update data
        }
        // Hilangkan pesan sukses setelah proses refresh dan jeda
        setTimeout(() => {
            checkoutSuccess.value = null;
        }, 3000); // Hilangkan setelah 3 detik
      }, 1500); // Tunda 1.5 detik untuk transisi
    } else {
      // Jika newOrder tidak memiliki ID, berarti ada masalah di aksi addOrder (misal: gagal response)
      checkoutError.value = orderStore.error?.message || 'Gagal memproses pembayaran. Silakan coba lagi.';
      console.warn("Checkout failed or response invalid:", orderStore.error);
      // Hilangkan pesan error setelah beberapa saat
      setTimeout(() => {
        checkoutError.value = null;
      }, 5000);
    }
  } catch (error) {
    // Tangani kesalahan jaringan atau kesalahan lain yang dilempar dari useApiFetch/addOrder
    checkoutError.value = error.message || 'Terjadi kesalahan tidak terduga saat memproses pembayaran. Periksa koneksi Anda.';
    console.error("Error during checkout process:", error);
    // Hilangkan pesan error setelah beberapa saat
    setTimeout(() => {
      checkoutError.value = null;
    }, 5000);
  } finally {
    processing.value = false; // Pastikan tombol diaktifkan kembali
  }
};
</script>

<style scoped>
.checkout-form-card {
  @apply bg-white p-6 rounded-xl shadow-lg border border-gray-100;
}

/* Custom animation for Total Amount display */
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-up {
  animation: fade-in-up 0.5s ease-out forwards;
}

/* General fade animation for messages */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* General fade-in for messages (using the previous animation) */
.animate-fade-in {
    animation: fade-in 0.4s ease-out forwards;
}
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Active state for button */
.transform.active\:scale-98:active {
    transform: scale(0.98);
}

/* Transisi Slide-down/up untuk input nominal tunai */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease-in-out;
  max-height: 100px; /* Cukup tinggi untuk input dan pesan kembalian */
  overflow: hidden;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
  max-height: 0;
  padding-top: 0; /* Pastikan padding juga dianimasikan */
  padding-bottom: 0;
}
</style>