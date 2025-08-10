<template>
  <Transition name="modal-fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-gray-900 bg-opacity-75 transition-opacity" @click="close"></div>
      
      <div class="bg-white rounded-lg shadow-xl p-6 transform transition-all duration-300 relative max-w-lg w-full z-10 scale-95 opacity-0 modal-fade-enter-to modal-fade-leave-from" :class="{ 'scale-100 opacity-100': isOpen }">
        <button 
          @click="close" 
          class="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-3xl font-bold transition-colors"
          aria-label="Tutup"
        >
          &times;
        </button>
        <slot></slot> </div>
    </div>
  </Transition>
</template>

<script setup>
import { watch } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};

// Menutup modal dengan tombol ESC
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    document.addEventListener('keydown', handleEsc);
  } else {
    document.removeEventListener('keydown', handleEsc);
  }
});

const handleEsc = (event) => {
  if (event.key === 'Escape') {
    close();
  }
};
</script>

<style scoped>
/* Transisi untuk modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-fade-enter-to,
.modal-fade-leave-active .modal-fade-leave-from {
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55); /* Spring-like effect */
}

/* Initial state for content (hidden) */
.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  transform: scale(0.95);
  opacity: 0;
}
</style>