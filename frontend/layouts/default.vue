<template>
  <div class="flex h-screen bg-gray-100">
    <div 
      v-if="isSidebarOpen && windowWidth < 768" 
      @click="toggleSidebar" 
      class="fixed inset-0 bg-black opacity-50 z-30 transition-opacity duration-300 ease-in-out"
    ></div>

    <aside
      :class="{
        'translate-x-0': isSidebarOpen,        // Sidebar terlihat
        '-translate-x-full': !isSidebarOpen,   // Sidebar tersembunyi ke kiri
        'md:translate-x-0': true               // Selalu terlihat di MD ke atas
      }"
      class="bg-gray-800 text-white w-64 fixed inset-y-0 left-0 z-40
             transition-transform duration-300 ease-in-out
             flex-shrink-0 overflow-y-auto"
    >
      <div class="p-4 flex flex-col h-full">
        <h1 class="text-2xl font-bold mb-6">Admin Dashboard</h1>
        
        <nav class="flex-grow">
          <ul>
            <li class="mb-2">
              <NuxtLink to="/admin" class="flex items-center p-2 rounded hover:bg-gray-700 transition-colors duration-200" active-class="bg-blue-600" @click="closeSidebarOnMobile">
                <Icon name="mdi:view-dashboard" class="mr-3" /> Dashboard
              </NuxtLink>
            </li>

            <li class="mb-2">
              <button 
                @click="toggleProductsMenu" 
                class="flex items-center justify-between w-full p-2 rounded hover:bg-gray-700 transition-colors duration-200 focus:outline-none"
                :class="{ 'bg-gray-700': isProductsMenuOpen || $route.path.startsWith('/admin/products') }"
              >
                <div class="flex items-center">
                  <Icon name="mdi:package-variant" class="mr-3" /> Produk
                </div>
                <Icon :name="isProductsMenuOpen ? 'mdi:chevron-down' : 'mdi:chevron-right'" class="w-5 h-5 transition-transform duration-200" />
              </button>
              
              <ul v-if="isProductsMenuOpen || $route.path.startsWith('/products')" class="ml-6 mt-1 space-y-1">
                <li>
                  <NuxtLink to="/products" 
                            class="flex items-center py-2 px-3 rounded-md hover:bg-gray-700 transition-colors duration-200 text-sm"
                            active-class="bg-blue-600" 
                            @click="closeSidebarOnMobile">
                    Daftar Produk
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink to="/products/add" 
                            class="flex items-center py-2 px-3 rounded-md hover:bg-gray-700 transition-colors duration-200 text-sm"
                            active-class="bg-blue-600" 
                            @click="closeSidebarOnMobile">
                    Tambah Produk
                  </NuxtLink>
                </li>
              </ul>
            </li>
            <li class="mb-2">
              <NuxtLink to="/orders" class="flex items-center p-2 rounded hover:bg-gray-700 transition-colors duration-200" active-class="bg-blue-600" @click="closeSidebarOnMobile">
                <Icon name="mdi:receipt-text-outline" class="mr-3" /> Transaksi
              </NuxtLink>
            </li>
            <li class="mb-2">
              <NuxtLink to="/admin/users" class="flex items-center p-2 rounded hover:bg-gray-700 transition-colors duration-200" active-class="bg-blue-600" @click="closeSidebarOnMobile">
                <Icon name="mdi:account-group" class="mr-3" /> Pengguna
              </NuxtLink>
            </li>
            </ul>
        </nav>

        <div v-if="authStore.isAuthenticated" class="mt-auto pt-4 border-t border-gray-700">
          <p class="text-sm mb-2">Logged in as: 
            <span class="font-bold">
              {{ authStore.user?.username || 'Guest' }}
            </span>
          </p> 
          <button @click="logout" class="w-full flex items-center p-2 rounded bg-red-600 hover:bg-red-700">
            <Icon name="mdi:logout" class="mr-3" /> Logout
          </button>
        </div>
      </div>
    </aside>

    <div class="flex-1 flex flex-col overflow-hidden">
      <header class="bg-white shadow p-4 flex justify-between items-center md:hidden">
        <button @click="toggleSidebar" class="text-gray-600 focus:outline-none">
          <Icon name="mdi:menu" class="text-3xl" />
        </button>
        <h2 class="text-xl font-bold">Admin Dashboard</h2>
      </header>

      <div
        :class="{
          'md:ml-64': true, 
          'ml-64': isSidebarOpen && windowWidth < 768,
          'ml-0': !isSidebarOpen && windowWidth < 768 // Penting untuk mobile saat sidebar tertutup
        }"
        class="flex-1 overflow-x-hidden overflow-y-auto transition-all duration-300 ease-in-out"
      >
        <main class="p-4">
          <NuxtPage />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'; // Tambahkan watch
import { useAuthStore } from '~/store/auth';
import { useRouter, useRoute } from 'vue-router'; // Tambahkan useRoute

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute(); // Dapatkan objek rute saat ini

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

// Toggle untuk sub-menu Produk
const toggleProductsMenu = () => {
  isProductsMenuOpen.value = !isProductsMenuOpen.value;
};

onMounted(() => {
  updateWindowWidth();
  if (process.client) {
    window.addEventListener('resize', updateWindowWidth);
  }
  // Atur status awal sub-menu Produk berdasarkan rute saat ini
  isProductsMenuOpen.value = route.path.startsWith('/admin/products');
});

onUnmounted(() => {
  if (process.client) {
    window.removeEventListener('resize', updateWindowWidth);
  }
});

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
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

// Watcher untuk route change: Tutup sidebar di mobile & buka sub-menu jika berada di jalur produk
watch(route, (newRoute) => {
  closeSidebarOnMobile(); // Selalu coba tutup sidebar di mobile saat navigasi
  isProductsMenuOpen.value = newRoute.path.startsWith('/admin/products'); // Otomatis buka sub-menu jika berada di jalur produk
});
</script>

<style scoped>
/* Pastikan ini menargetkan NuxtLink secara umum atau gunakan kelas aktif khusus */
.router-link-active,
.router-link-exact-active {
  background-color: #4a5568; /* Warna latar belakang untuk link aktif */
}

/* Kustomisasi untuk link aktif di dalam sub-menu */
.ml-6 .router-link-active,
.ml-6 .router-link-exact-active {
  background-color: #2b6cb0; /* Warna biru untuk sub-link aktif, agar menonjol dari parent */
}
</style>