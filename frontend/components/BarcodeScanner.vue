<template>
  <div class="barcode-scanner-container p-4">
    
    <div v-if="loading" class="text-center text-gray-600 py-10">
      <p class="text-lg mb-2">Memuat kamera...</p>
      <div class="loader-sm mx-auto mt-4"></div>
    </div>
    <div v-else-if="error" class="text-center text-red-600 py-10">
      <Icon name="mdi:alert-circle" class="text-red-500 text-4xl mb-2" />
      <p class="text-base font-medium mb-1">Error Kamera:</p>
      <p class="text-sm">{{ error }}</p>
      <p class="text-sm mt-2">Pastikan Anda memberikan izin kamera.</p>
    </div>
    <div v-else class="text-center text-gray-700 text-sm mb-3">
      <p>Arahkan kamera ke barcode.</p>
    </div>

   
    <video
      v-show="!loading && !error" 
      ref="videoElement"
      class="w-full h-auto rounded-lg shadow-md border border-gray-200 bg-gray-800"
      autoplay
      muted
      playsinline
    ></video>
    
    <p v-if="!loading && !error" class="text-center text-gray-500 text-xs mt-2">Pastikan barcode terlihat jelas di area pemindaian.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';
import { BrowserMultiFormatReader, NotFoundException } from '@zxing/library';

const emit = defineEmits(['scan-success', 'scan-error', 'close']);

const videoElement = ref(null);
const codeReader = ref(null);
const loading = ref(true); // Awalnya set loading ke true
const error = ref(null);

const props = defineProps({
  isActive: {
    type: Boolean,
    default: false
  }
});

const startScanner = async () => {
  loading.value = true; // Set loading ke true saat memulai
  error.value = null;
  codeReader.value = new BrowserMultiFormatReader(); 

  try {
    // Tunggu nextTick untuk memastikan elemen video sudah ada di DOM
    // Karena v-show, elemen video akan selalu ada di DOM saat komponen ini di-mount
    await nextTick(); 
    if (!videoElement.value) {
      // Ini seharusnya tidak terpicu dengan v-show, tapi tetap sebagai safeguard
      throw new Error("Elemen video tidak tersedia di DOM setelah nextTick.");
    }

    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoInputDevices = devices.filter(device => device.kind === 'videoinput');
    
    if (videoInputDevices.length === 0) {
      throw new Error("Tidak ada kamera ditemukan.");
    }

    const selectedDeviceId = videoInputDevices[0].deviceId; 

    // Gunakan decodeFromVideoDevice() yang akan mengelola getUserMedia dan play() secara internal
    codeReader.value.decodeFromVideoDevice(selectedDeviceId, videoElement.value, (result, err) => {
      if (result) {
        console.log('Barcode scanned:', result.getText());
        emit('scan-success', result.getText());
        stopScanner(); // Hentikan scanner setelah berhasil
      }
      if (err && !(err instanceof NotFoundException)) {
        console.error('Scan error (not NotFoundException):', err); // Log error spesifik
      } else if (err instanceof NotFoundException) {
        // console.log('No barcode found in current frame.'); // Opsional: log jika tidak ada barcode ditemukan
      }
    });

    console.log('Scanner started with device:', selectedDeviceId);
    loading.value = false; // Set loading ke false setelah scanner berhasil dimulai

  } catch (err) {
    console.error('Error accessing camera:', err);
    let errorMessage = 'Gagal mengakses kamera.';
    if (err.name === 'NotAllowedError') {
      errorMessage = 'Izin kamera ditolak. Harap izinkan akses kamera di pengaturan browser Anda.';
    } else if (err.name === 'NotFoundError' || err.message === 'Tidak ada kamera ditemukan.') {
      errorMessage = 'Tidak ada kamera yang terdeteksi atau tersedia.';
    } else if (err.name === 'NotReadableError') {
      errorMessage = 'Kamera sedang digunakan oleh aplikasi lain atau tidak dapat diakses.';
    } else if (err.name === 'OverconstrainedError') {
      errorMessage = 'Kamera tidak dapat memenuhi batasan yang diminta (mis. resolusi).';
    } else if (err.message === "Elemen video tidak tersedia di DOM.") {
        errorMessage = "Terjadi masalah internal dengan elemen video. Coba refresh halaman.";
    }
    else {
      errorMessage += ' ' + err.message;
    }
    error.value = errorMessage;
    loading.value = false; // Pastikan loading false jika ada error
    emit('scan-error', error.value);
  }
};

const stopScanner = () => {
  if (codeReader.value) {
    codeReader.value.reset(); // Menghentikan decoding dan membersihkan resources
    console.log('Scanner stopped.');
  }
};

// --- Lifecycle Hooks ---
onMounted(() => {
  // Hanya panggil startScanner jika isActive true saat mount
  if (props.isActive) {
    startScanner();
  }
});

onUnmounted(() => {
  stopScanner();
});

// --- Watcher untuk mengontrol scanner saat isActive berubah ---
watch(() => props.isActive, (newVal) => {
  if (newVal) {
    // Reset states dan mulai scanner saat isActive menjadi true
    loading.value = true;
    error.value = null;
    startScanner();
  } else {
    // Hentikan scanner saat isActive menjadi false
    stopScanner();
  }
});
</script>

<style scoped>
.barcode-scanner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 250px; /* Minimum height for scanner area */
}
video {
  max-width: 100%;
  height: auto;
  display: block;
  /* Add a min-height to ensure the video element has space even if no stream */
  min-height: 150px; /* Adjust as needed */
  background-color: #333; /* Dark background for visibility before stream starts */
}
.loader-sm {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #8B5CF6; /* Purple-500 */
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
