<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <div 
      v-if="isSidebarOpen && windowWidth < 768" 
      @click="toggleSidebar" 
      class="fixed inset-0 bg-black opacity-50 z-30 transition-opacity duration-300 ease-in-out"
    ></div>

    <header class="bg-white shadow p-4 flex justify-between items-center md:hidden z-20">
      <button @click="toggleSidebar" class="text-gray-600 focus:outline-none">
        <Icon name="mdi:menu" class="text-3xl" />
      </button>
      <h2 class="text-xl font-bold">CashierApp</h2>
      <div v-if="authStore.isAuthenticated" class="flex items-center gap-2 text-sm text-gray-700">
        <Icon name="mdi:account-circle" class="text-2xl" />
        <span class="font-semibold">{{ authStore.user?.username || 'Guest' }}</span>
        <button @click="logout" class="text-red-600 hover:text-red-800 ml-2">
          <Icon name="mdi:logout" class="text-xl" />
        </button>
      </div>
      <div v-else>
        <NuxtLink to="/login" class="text-blue-600 hover:text-blue-800 font-semibold text-sm">Login</NuxtLink>
      </div>
    </header>

    <nav class="hidden md:flex bg-gray-800 text-white p-4 items-center justify-between shadow-lg z-20">
      <div class="flex items-center">
        <h1 class="text-2xl font-bold mr-8">CashierApp</h1>
        <ul class="flex space-x-6">
          <li>
            <NuxtLink to="/" class="flex items-center p-2 rounded hover:bg-gray-700 transition-colors duration-200" active-class="bg-blue-600">
              <Icon name="mdi:view-dashboard" class="mr-2" /> Dashboard
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/orders" class="flex items-center p-2 rounded hover:bg-gray-700 transition-colors duration-200" active-class="bg-blue-600">
              <Icon name="mdi:receipt-text-outline" class="mr-2" /> Transaksi
            </NuxtLink>
          </li>
          </ul>
      </div>

      <div v-if="authStore.isAuthenticated" class="flex items-center gap-4">
        <p class="text-sm">Logged in as: 
          <span class="font-bold">
            {{ authStore.user?.username || 'Guest' }}
          </span>
        </p> 
        <button @click="logout" class="flex items-center p-2 rounded bg-red-600 hover:bg-red-700 transition-colors duration-200">
          <Icon name="mdi:logout" class="mr-2" /> Logout
        </button>
      </div>
      <div v-else>
        <NuxtLink to="/login" class="flex items-center p-2 rounded bg-blue-600 hover:bg-blue-700 transition-colors duration-200">
          <Icon name="mdi:login" class="mr-2" /> Login
        </NuxtLink>
      </div>
    </nav>

    <aside
      :class="{
        'translate-x-0': isSidebarOpen,
        '-translate-x-full': !isSidebarOpen,
      }"
      class="bg-gray-800 text-white w-64 fixed inset-y-0 left-0 z-40
             transition-transform duration-300 ease-in-out
             flex-shrink-0 overflow-y-auto md:hidden"
    >
      <div class="p-4 flex flex-col h-full">
        <h1 class="text-2xl font-bold mb-6">CashierApp</h1>
        <nav class="flex-grow">
          <ul>
            <li class="mb-2">
              <NuxtLink to="/" class="flex items-center p-2 rounded hover:bg-gray-700 transition-colors duration-200" active-class="bg-blue-600" @click="closeSidebarOnMobile">
                <Icon name="mdi:view-dashboard" class="mr-3" /> Dashboard
              </NuxtLink>
            </li>
            <li class="mb-2">
              <NuxtLink to="/orders" class="flex items-center p-2 rounded hover:bg-gray-700 transition-colors duration-200" active-class="bg-blue-600" @click="closeSidebarOnMobile">
                <Icon name="mdi:receipt-text-outline" class="mr-3" /> Transaksi
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
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4">
        <NuxtPage />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '~/store/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const isSidebarOpen = ref(false);
const windowWidth = ref(0);

const updateWindowWidth = () => {
  if (process.client) {
    windowWidth.value = window.innerWidth;
    // Sidebar hanya terbuka secara default di desktop jika layoutnya sidebar,
    // tapi karena kita ingin navbar di desktop, kita tidak perlu ini lagi.
    // Kita hanya perlu memastikan isSidebarOpen false di desktop.
    if (window.innerWidth >= 768) {
      isSidebarOpen.value = false; // Pastikan sidebar tertutup di desktop
    }
  }
};

onMounted(() => {
  updateWindowWidth();
  if (process.client) {
    window.addEventListener('resize', updateWindowWidth);
  }
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
</script>

<style scoped>
/* Pastikan ini menargetkan NuxtLink di navbar/sidebar Anda */
.router-link-active {
  background-color: #3b82f6; /* Warna biru untuk active link, sesuaikan jika perlu */
  color: white; /* Pastikan teks tetap putih */
}

/* Jika Anda ingin warna berbeda untuk exact active link (misal hanya '/' saja) */
.router-link-exact-active {
  background-color: #2563eb; /* Warna biru yang lebih gelap */
}

/* Penyesuaian untuk main content agar tidak tumpang tindih dengan sidebar di mobile */
/* Main content tidak lagi memiliki md:ml-64 karena tidak ada sidebar tetap di desktop */
/* Namun, kita perlu mendorongnya jika sidebar mobile terbuka */
main {
  /* Untuk memastikan main content dimulai setelah navbar */
  padding-top: 1rem; /* Sesuaikan dengan tinggi navbar Anda */
}

@media (min-width: 768px) { /* Medium screens and up */
  main {
    padding-top: 0; /* No padding-top needed as navbar is fixed to top */
  }
}

/* Override NuxtLink default styling jika ada */
a {
  text-decoration: none;
}
</style>