<template>
  <div class="product-card">
    <div class="relative overflow-hidden rounded-xl h-48 mb-4">
      <img 
        v-if="product.image" 
        :src="product.image" 
        :alt="product.name" 
        class="w-full h-full object-cover transform transition-transform duration-300 group-hover:scale-105"
        @error="handleImageError"
      > <!-- Menggunakan computed property untuk URL gambar -->
      <div v-else class="w-full h-full bg-gray-200 flex items-center justify-center text-gray-500 text-sm italic">
        Tidak ada gambar
      </div>

      <div v-if="product.stock === 0" class="absolute top-2 left-2 bg-red-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md animate-pulse">
        STOK HABIS
      </div>
      <div v-else-if="product.stock < 10 && product.stock > 0" class="absolute top-2 left-2 bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md">
        STOK RENDAH! ({{ product.stock }})
      </div>
      <div v-else-if="product.stock >= 10" class="absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md">
        STOK TERSISA ({{ product.stock }})
      </div>
    </div> 

    <div class="p-2 flex-grow flex flex-col justify-between">
      <div>
        <h3 class="text-xl font-bold text-gray-900 mb-1 leading-tight">{{ product.name }}</h3>
        <p class="text-gray-600 text-sm mb-2">{{ product.category_name }}</p>
        <p class="text-blue-700 font-extrabold text-2xl mb-3">Rp {{ product.price?.toLocaleString('id-ID') || '0' }}</p>
      </div>

      <button
        @click="handleAddToCart"
        :disabled="product.stock === 0 || isAdding"
        class="w-full py-3 px-4 rounded-lg font-semibold text-lg transition-all duration-300 ease-in-out
               flex items-center justify-center gap-2 group transform active:scale-95"
        :class="{
          'bg-blue-600 text-white hover:bg-blue-700 shadow-md': product.stock > 0,
          'bg-gray-400 text-gray-700 cursor-not-allowed': product.stock === 0,
          'opacity-75': isAdding // Efek saat loading
        }"
      >
      
        <template v-if="isAdding">
          <Icon name="mdi:loading" class="animate-spin text-xl" /> Menambahkan...
        </template>
        <template v-else>
          <Icon name="mdi:cart-plus" class="text-xl group-hover:scale-110 transition-transform" /> 
          {{ product.stock === 0 ? 'Stok Habis' : 'Tambah ke Keranjang' }}
        </template>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'; // Import computed
import { useCartStore } from '~/store/cart';
// useProductStore tidak diperlukan di sini karena kita meneruskan objek produk lengkap
// import { useProductStore } from '~/store/products'; 

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

const cartStore = useCartStore();
// const productStore = useProductStore(); // Tidak diperlukan lagi
const isAdding = ref(false); // State untuk loading tombol

 // Diperlukan untuk URL gambar



const handleImageError = (event) => {
  // Ganti gambar dengan placeholder jika terjadi error loading
  event.target.src = 'https://placehold.co/400x300/E0E0E0/808080?text=Image+Error';
};


// Mengubah nama fungsi lokal menjadi handleAddToCart agar lebih jelas
const handleAddToCart = async () => {
  // Mencegah klik ganda atau jika stok habis
  if (isAdding.value || props.product.stock === 0) return; 

  isAdding.value = true;
  try {
    // Panggil aksi addToCart dari cartStore, TERUSKAN OBJEK PRODUK LENGKAP
    await cartStore.addToCart(props.product); 
    
    // Opsional: Tampilkan notifikasi sukses
    // alert(`"${props.product.name}" berhasil ditambahkan ke keranjang!`);

  } catch (error) {
    console.error("Gagal menambahkan ke keranjang:", error);
    alert("Gagal menambahkan produk ke keranjang. Silakan coba lagi."); // Tampilkan notifikasi error
  } finally {
    isAdding.value = false;
  }
};
</script>

<style scoped>
.product-card {
  @apply bg-white border border-gray-200 rounded-xl shadow-lg 
         flex flex-col overflow-hidden cursor-pointer 
         transform hover:scale-[1.02] transition-all duration-300 ease-in-out;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

/* Custom fade-in for stock badges or other dynamic elements */
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
  animation: fade-in-up 0.4s ease-out forwards;
}

/* Animate pulse for stock-out badge */
.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .7;
  }
}
</style>
