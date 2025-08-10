<template>
  <div class="container mx-auto px-4 py-6 bg-gray-50 min-h-screen">
    <div class="bg-white p-6 rounded-2xl shadow-xl border border-gray-100 mb-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-5 gap-4">
        <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-3 flex-shrink-0">
          <Icon name="mdi:account-group-outline" class="text-indigo-600 text-3xl" />
          Manajemen Pengguna
        </h1>

        <div class="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto flex-wrap justify-end">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Cari nama pengguna..."
            class="flex-1 min-w-[180px] w-full sm:w-64 px-4 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-base placeholder-gray-500 transition duration-200"
          />
          <NuxtLink to="/admin/users/add" 
            class="px-5 py-2.5 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition duration-200 ease-in-out transform active:scale-95 flex items-center justify-center gap-2">
            <Icon name="mdi:plus-circle-outline" class="text-xl" /> Tambah Pengguna Baru
          </NuxtLink>
        </div>
      </div>

      <div v-if="successMessage" class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-4 rounded-md animate-fade-in" role="alert">
        <div class="flex items-center">
          <Icon name="mdi:check-circle-outline" class="mr-3 text-green-600 text-xl" />
          <p class="font-bold">{{ successMessage }}</p>
        </div>
      </div>
      <div v-if="errorMessages.general" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4 rounded-md animate-fade-in" role="alert">
        <div class="flex items-center">
          <Icon name="mdi:alert-circle-outline" class="mr-3 text-red-600 text-xl" />
          <p class="font-bold">{{ errorMessages.general }}</p>
        </div>
      </div>

      <div v-if="loading" class="text-center text-gray-600 py-20">
        <p class="text-xl font-medium mb-4 animate-pulse">Memuat daftar pengguna...</p>
        <div class="loader-lg mt-4"></div>
      </div>
      <div v-else-if="filteredUsers.length === 0" class="text-center text-gray-500 py-20">
        <Icon name="mdi:account-off-outline" class="text-gray-400 text-5xl mb-3" />
        <p class="text-xl font-medium">Tidak Ada Pengguna Ditemukan</p>
        <p class="text-sm mt-2" v-if="searchQuery">Tidak ada pengguna yang cocok dengan "{{ searchQuery }}". Coba kata kunci lain.</p>
        <p class="text-sm mt-2" v-else>Tambahkan pengguna baru untuk memulai.</p>
      </div>
      <div v-else>
        <div class="overflow-x-auto bg-white shadow-md rounded-lg border border-gray-200">
          <table class="min-w-full leading-normal">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-200">
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Username
                </th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Email
                </th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Peran
                </th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Aktif
                </th>
                <th class="px-5 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Aksi
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id" class="border-b border-gray-100 hover:bg-gray-50 transition-colors duration-150">
                <td class="px-5 py-4 bg-white text-sm">
                  <p class="text-gray-900 font-medium">{{ user.username }}</p>
                </td>
                <td class="px-5 py-4 bg-white text-sm">
                  <p class="text-gray-700">{{ user.email || '-' }}</p>
                </td>
                <td class="px-5 py-4 bg-white text-sm">
                  <div class="flex flex-wrap gap-1">
                    <span v-for="group in user.groups" :key="group" class="inline-flex items-center bg-indigo-100 text-indigo-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                      <Icon name="mdi:label" class="mr-1" /> {{ group }}
                    </span>
                    <span v-if="user.is_superuser" class="inline-flex items-center bg-purple-100 text-purple-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                      <Icon name="mdi:crown" class="mr-1" /> Superuser
                    </span>
                  </div>
                </td>
                <td class="px-5 py-4 bg-white text-sm">
                  <span :class="{'text-green-600 font-semibold': user.is_active, 'text-red-600 font-semibold': !user.is_active}" class="flex items-center gap-1">
                    <Icon :name="user.is_active ? 'mdi:check-circle' : 'mdi:close-circle'" class="text-lg" />
                    {{ user.is_active ? 'Ya' : 'Tidak' }}
                  </span>
                </td>
                <td class="px-5 py-4 bg-white text-sm">
                  <div class="flex items-center space-x-3">
                    <NuxtLink :to="`/admin/users/${user.id}/edit`" 
                      class="text-blue-600 hover:text-blue-800 flex items-center gap-1 transition-colors duration-200">
                      <Icon name="mdi:pencil-outline" class="text-lg" /> Edit
                    </NuxtLink>
                    <button @click="confirmDelete(user.id)" 
                      class="text-red-600 hover:text-red-800 flex items-center gap-1 transition-colors duration-200">
                      <Icon name="mdi:delete-outline" class="text-lg" /> Hapus
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <Modal :is-open="showDeleteConfirmModal" @close="cancelDelete">
      <div class="text-center p-4">
        <Icon name="mdi:alert-circle-outline" class="text-red-500 text-6xl mb-4 animate-bounce-in" />
        <h3 class="text-xl font-semibold text-gray-800 mb-3">Konfirmasi Hapus Pengguna</h3>
        <p class="text-gray-600 mb-5">Apakah Anda yakin ingin menghapus pengguna ini secara permanen? Tindakan ini tidak bisa dibatalkan.</p>
        <div class="flex justify-center gap-4">
          <button @click="cancelDelete" 
            class="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100 transition duration-200">Batal</button>
          <button @click="deleteUserConfirmed" 
            class="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition duration-200">Hapus</button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'; // Import computed
import { useAuthStore } from '~/store/auth'; 
import { useRuntimeConfig } from '#app'; 
import Modal from '~/components/Modal.vue'; 

// --- Pinia Stores ---
const authStore = useAuthStore();

// --- Runtime Config ---
const runtimeConfig = useRuntimeConfig();
const API_BASE_URL = runtimeConfig.public.apiBaseUrl;

// --- State Reaktif ---
const users = ref([]);
const loading = ref(false);
const errorMessages = ref({});
const successMessage = ref('');

// State untuk pencarian
const searchQuery = ref('');

// State untuk modal konfirmasi hapus
const showDeleteConfirmModal = ref(false);
const userIdToDelete = ref(null);

// --- Computed Property untuk Filter Pengguna ---
const filteredUsers = computed(() => {
  if (!users.value) {
    return [];
  }
  const query = searchQuery.value.toLowerCase().trim();
  if (!query) {
    return users.value; // Jika query kosong, kembalikan semua pengguna
  }
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) ||
    (user.email && user.email.toLowerCase().includes(query)) // Juga cari berdasarkan email jika ada
  );
});


// --- Fungsi Pengambilan Data ---
const fetchUsers = async () => {
  loading.value = true;
  errorMessages.value = {};
  successMessage.value = ''; // Clear messages on new fetch
  try {
    const response = await $fetch(`${API_BASE_URL}users/`, {
      headers: {
        'Authorization': `Token ${authStore.token}`,
      },
    });
    users.value = response;
  } catch (error) {
    console.error('Error fetching users:', error);
    errorMessages.value.general = 'Gagal memuat pengguna. Silakan periksa izin.';
  } finally {
    loading.value = false;
  }
};

// --- Fungsi Hapus Pengguna (dipicu dari modal) ---
const confirmDelete = (userId) => {
  userIdToDelete.value = userId;
  showDeleteConfirmModal.value = true;
};

const cancelDelete = () => {
  showDeleteConfirmModal.value = false;
  userIdToDelete.value = null;
};

const deleteUserConfirmed = async () => {
  if (!userIdToDelete.value) return;

  loading.value = true;
  errorMessages.value = {};
  successMessage.value = '';
  showDeleteConfirmModal.value = false; // Tutup modal saat delete dimulai

  try {
    await $fetch(`${API_BASE_URL}users/${userIdToDelete.value}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${authStore.token}`,
      },
    });
    successMessage.value = 'Pengguna berhasil dihapus.';
    userIdToDelete.value = null; // Reset ID
    fetchUsers(); // Refresh daftar pengguna
  } catch (error) {
    console.error('Error deleting user:', error);
    errorMessages.value.general = 'Gagal menghapus pengguna. Periksa izin atau coba lagi.';
  } finally {
    loading.value = false;
  }
};

// --- Lifecycle Hooks ---
onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
/* Tambahan styling untuk loader dan animasi */
.loader-lg {
  border: 6px solid #e0e0e0;
  border-top: 6px solid #6366f1; /* Indigo-500 */
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 1.5s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.3s ease-out forwards;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}
.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes bounce-in {
  0% { transform: scale(0.5); opacity: 0; }
  70% { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(1); }
}
.animate-bounce-in {
  animation: bounce-in 0.5s ease-out forwards;
}

/* Tabel styling */
table {
  border-collapse: collapse;
}

th, td {
  padding: 1rem 1.25rem; /* px-5 py-3/4 */
  vertical-align: middle;
}

tbody tr:last-child {
  border-bottom: none; /* No border for the last row */
}
</style>