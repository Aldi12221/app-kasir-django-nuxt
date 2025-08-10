<template>
  <div class="flex h-screen bg-gray-100 font-sans">
    <div 
      v-if="isSidebarOpen && windowWidth < 768" 
      @click="toggleSidebar" 
      class="fixed inset-0 bg-black bg-opacity-60 z-30 transition-opacity duration-300 ease-in-out"
    ></div>

    <aside
      :class="{
        'translate-x-0': isSidebarOpen,          // Sidebar terlihat
        '-translate-x-full': !isSidebarOpen,     // Sidebar tersembunyi ke kiri
        'md:translate-x-0': true                 // Selalu terlihat di MD ke atas
      }"
      class="bg-gray-800 text-white w-64 fixed inset-y-0 left-0 z-40
             transition-transform duration-300 ease-in-out
             flex-shrink-0 overflow-y-auto shadow-lg"
    >
      <div class="p-6 flex flex-col h-full">
        <div class="flex items-center mb-8 pb-4 border-b border-gray-700">
          <Icon name="mdi:cog-box" class="text-blue-400 text-4xl mr-3" />
          <h1 class="text-2xl font-extrabold text-blue-300">AdminPanel</h1>
        </div>
        
        <nav class="flex-grow space-y-2">
          <ul>
            <li class="mb-2">
              <NuxtLink 
                to="/admin" 
                class="flex items-center p-3 rounded-lg hover:bg-gray-700 transition-colors duration-200 text-lg font-medium group" 
                active-class="bg-blue-600 shadow-md text-white" 
                @click="closeSidebarOnMobile"
              >
                <Icon name="mdi:view-dashboard" class="mr-4 text-xl group-hover:scale-110 transition-transform" /> Dashboard
              </NuxtLink>
            </li>

            <li class="mb-2">
              <button 
                @click="toggleProductsMenu" 
                class="flex items-center justify-between w-full p-3 rounded-lg hover:bg-gray-700 transition-colors duration-200 focus:outline-none text-lg font-medium group"
                :class="{ 'bg-gray-700': isProductsMenuOpen || $route.path.startsWith('/admin/products') }"
              >
                <div class="flex items-center">
                  <Icon name="mdi:package-variant" class="mr-4 text-xl group-hover:scale-110 transition-transform" /> Produk
                </div>
                <Icon :name="isProductsMenuOpen ? 'mdi:chevron-down' : 'mdi:chevron-right'" class="w-6 h-6 transition-transform duration-200" />
              </button>
              
              <transition name="fade-slide">
                <ul v-if="isProductsMenuOpen || $route.path.startsWith('/admin/products')" class="ml-8 mt-2 space-y-1 bg-gray-700 rounded-lg py-2">
                  <li>
                    <NuxtLink 
                      to="/products" 
                      class="flex items-center py-2 px-4 rounded-md hover:bg-gray-600 transition-colors duration-200 text-base font-normal group"
                      active-class="bg-blue-500 text-white" 
                      @click="closeSidebarOnMobile"
                    >
                      <Icon name="mdi:format-list-bulleted" class="mr-3 text-lg group-hover:scale-110 transition-transform" /> Daftar Produk
                    </NuxtLink>
                  </li>
                  <li>
                    <NuxtLink 
                      to="/products/add" 
                      class="flex items-center py-2 px-4 rounded-md hover:bg-gray-600 transition-colors duration-200 text-base font-normal group"
                      active-class="bg-blue-500 text-white" 
                      @click="closeSidebarOnMobile"
                    >
                      <Icon name="mdi:plus-box-multiple-outline" class="mr-3 text-lg group-hover:scale-110 transition-transform" /> Tambah Produk
                    </NuxtLink>
                  </li>
                </ul>
              </transition>
            </li>

            <li class="mb-2">
              <NuxtLink 
                to="/admin/orders" 
                class="flex items-center p-3 rounded-lg hover:bg-gray-700 transition-colors duration-200 text-lg font-medium group" 
                active-class="bg-blue-600 shadow-md text-white" 
                @click="closeSidebarOnMobile"
              >
                <Icon name="mdi:receipt-text-outline" class="mr-4 text-xl group-hover:scale-110 transition-transform" /> Transaksi
              </NuxtLink>
            </li>

            <li class="mb-2">
              <NuxtLink 
                to="/admin/users" 
                class="flex items-center p-3 rounded-lg hover:bg-gray-700 transition-colors duration-200 text-lg font-medium group" 
                active-class="bg-blue-600 shadow-md text-white" 
                @click="closeSidebarOnMobile"
              >
                <Icon name="mdi:account-group" class="mr-4 text-xl group-hover:scale-110 transition-transform" /> Pengguna
              </NuxtLink>
            </li>
          </ul>
        </nav>

        <div v-if="authStore.isAuthenticated" class="mt-auto pt-6 border-t border-gray-700">
          <div class="flex items-center mb-4">
            <Icon name="mdi:account-circle" class="text-gray-400 text-3xl mr-3" />
            <div>
              <p class="text-sm text-gray-400">Login sebagai:</p>
              <p class="font-bold text-lg text-blue-200">{{ authStore.user?.username || 'Guest' }}</p>
            </div>
          </div>
          <button 
            @click="logout" 
            class="w-full flex items-center justify-center p-3 rounded-lg bg-red-600 hover:bg-red-700 text-white font-semibold transition-colors duration-200 shadow-md transform active:scale-95"
          >
            <Icon name="mdi:logout" class="mr-3 text-xl" /> Logout
          </button>
        </div>
      </div>
    </aside>

    <div 
      :class="{
        'md:ml-64': true, 
        'ml-64': isSidebarOpen && windowWidth < 768,
        'ml-0': !isSidebarOpen && windowWidth < 768 // Penting untuk mobile saat sidebar tertutup
      }"
      class="flex-1 flex flex-col transition-all duration-300 ease-in-out"
    >
      <header class="bg-white shadow-sm p-4 flex justify-between items-center md:hidden">
        <button @click="toggleSidebar" class="text-gray-700 hover:text-gray-900 focus:outline-none transform active:scale-95 transition-transform">
          <Icon name="mdi:menu" class="text-3xl" />
        </button>
        <h2 class="text-xl font-extrabold text-gray-800">Admin Dashboard</h2>
      </header>

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-6 bg-gray-100">
        <NuxtPage />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useAuthStore } from '~/store/auth';
import { useRouter, useRoute } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const isSidebarOpen = ref(false);
const windowWidth = ref(0);
const isProductsMenuOpen = ref(false); // State untuk sub-menu Produk

const updateWindowWidth = () => {
  if (process.client) {
    windowWidth.value = window.innerWidth;
    if (window.innerWidth >= 768) {
      isSidebarOpen.value = true; // Selalu buka sidebar di desktop
    } else {
      isSidebarOpen.value = false; // Selalu tutup sidebar di mobile secara default
    }
  }
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

// Toggle untuk sub-menu Produk
const toggleProductsMenu = () => {
  isProductsMenuOpen.value = !isProductsMenuOpen.value;
};

const closeSidebarOnMobile = () => {
  if (windowWidth.value < 768) {
    isSidebarOpen.value = false;
  }
};

const logout = async () => {
  await authStore.logout();
  router.push('/login');
};

onMounted(() => {
  updateWindowWidth();
  if (process.client) {
    window.addEventListener('resize', updateWindowWidth);
  }
  // Atur status awal sub-menu Produk berdasarkan rute saat ini saat mount
  isProductsMenuOpen.value = route.path.startsWith('/admin/products');
});

onUnmounted(() => {
  if (process.client) {
    window.removeEventListener('resize', updateWindowWidth);
  }
});

// Watcher untuk route change: Tutup sidebar di mobile & buka sub-menu jika berada di jalur produk
watch(route, (newRoute) => {
  closeSidebarOnMobile(); // Selalu coba tutup sidebar di mobile saat navigasi
  isProductsMenuOpen.value = newRoute.path.startsWith('/admin/products'); // Otomatis buka sub-menu jika berada di jalur produk
});
</script>

<style scoped>
/* Transisi Fade & Slide untuk Sub-menu */
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.3s ease-out;
  max-height: 100px; /* Batasan tinggi untuk transisi */
  overflow: hidden;
}
.fade-slide-enter-from, .fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

/* Base Styling for NuxtLink & Button */
.nav-link-base {
  @apply flex items-center p-3 rounded-lg transition-colors duration-200 text-lg font-medium;
}

/* Active Class for Main Nav Links */
.bg-blue-600.shadow-md.text-white {
    background-color: #2563eb; /* Biru yang lebih kuat untuk aktif */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Active Class for Sub-Nav Links */
.ml-8 .bg-blue-500.text-white {
    background-color: #3b82f6; /* Biru yang sedikit lebih terang untuk sub-aktif */
}

/* Hover effect for all nav items */
.group:hover .group-hover\:scale-110 {
    transform: scale(1.1);
}

/* Active state for products dropdown button when its sub-links are active */
.bg-gray-700 {
    background-color: #4a5568; /* Warna abu-abu gelap untuk tombol produk saat terbuka/aktif */
}

/* Style for main content area to prevent scrollbar issues */
main {
  min-height: calc(100vh - 64px); /* Sesuaikan dengan tinggi header jika ada */
}

/* Custom scrollbar for sidebar if needed */
aside::-webkit-scrollbar {
  width: 8px;
}
aside::-webkit-scrollbar-track {
  background: #374151; /* Warna track lebih gelap */
  border-radius: 10px;
}
aside::-webkit-scrollbar-thumb {
  background: #6b7280; /* Warna thumb lebih gelap */
  border-radius: 10px;
}
aside::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>