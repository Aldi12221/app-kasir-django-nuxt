<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-2xl transform transition-all duration-300 scale-95 opacity-0 animate-scale-in">
      <h3 class="text-2xl font-bold text-green-700 mb-4 flex items-center gap-3">
        <Icon name="mdi:check-decagram-outline" class="text-3xl" />
        Transaksi Berhasil!
      </h3>
      <p class="text-gray-700 mb-4">Order Anda dengan ID **#{{ order?.id }}** telah berhasil diproses.</p>

      <div class="border-t border-b border-gray-200 py-3 mb-4">
        <p class="text-gray-600 mb-1">Total Pembelian:</p>
        <p class="text-green-800 font-bold text-2xl mb-2">Rp {{ order?.total_amount.toLocaleString('id-ID') }}</p>
        <p class="text-gray-600 text-sm">Metode Pembayaran: <span class="font-semibold">{{ formatPaymentMethod(order?.payment_method) }}</span></p>
        <p v-if="order?.cash_amount" class="text-gray-600 text-sm">Nominal Bayar: <span class="font-semibold">Rp {{ order?.cash_amount.toLocaleString('id-ID') }}</span></p>
        <p v-if="order?.cash_amount && order.cash_amount - order.total_amount >= 0" class="text-gray-600 text-sm">Kembali: <span class="font-semibold">Rp {{ (order.cash_amount - order.total_amount).toLocaleString('id-ID') }}</span></p>
        <p v-if="order?.notes" class="text-gray-600 text-sm mt-2">Catatan: <span class="italic">{{ order?.notes }}</span></p>
      </div>

      <h4 class="text-lg font-semibold text-gray-800 mb-2">Item Pembelian:</h4>
      <ul class="max-h-32 overflow-y-auto mb-4 border border-gray-200 rounded p-2 custom-scrollbar">
        <li v-for="item in order?.items" :key="item.product_id" class="text-sm text-gray-800 py-0.5">
          {{ item.quantity }}x {{ item.product_name || 'Produk Tidak Dikenal' }} @ Rp {{ item.price_at_order.toLocaleString('id-ID') }}
        </li>
      </ul>

      <button
        @click="$emit('close')"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 px-5 rounded-lg shadow-md transition duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Selesai
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  order: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['close']);

const formatPaymentMethod = (method) => {
  switch (method) {
    case 'cash': return 'Tunai';
    case 'qris': return 'QRIS';
    case 'bank_transfer': return 'Transfer Bank';
    default: return method;
  }
};
</script>

<style scoped>
/* Animasi untuk modal */
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

/* Custom Scrollbar for items list */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}
</style>