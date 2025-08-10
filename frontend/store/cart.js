import { defineStore } from 'pinia';
// useProductStore tidak lagi diperlukan di sini untuk addToCart/updateQuantity
// karena kita akan melewati objek produk lengkap.
// import { useProductStore } from '~/store/products'; 
import { useApiClient } from '~/composables/useApiFetch'; // Import useApiClient untuk checkout

export const useCartStore = defineStore('cart', {
    state: () => ({
        // Format item di keranjang akan menyimpan detail produk yang diperlukan
        // untuk menghindari pencarian ulang di productStore
        items: [], // Array of cart items { id, name, price, quantity, stock, image, ...other_product_details }
    }),

    getters: {
        totalItems: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
        totalAmount: (state) => {
            const total = state.items.reduce((sum, item) => {
                // Pastikan item.price adalah angka sebelum perhitungan
                const price = parseFloat(item.price);
                return sum + (item.quantity * (isNaN(price) ? 0 : price));
            }, 0);
            return total;
        },
        getItemById: (state) => (productId) => {
            return state.items.find(item => item.id === productId);
        },
    },

    actions: {
        /**
         * Menambahkan produk ke keranjang atau menambah kuantitasnya jika sudah ada.
         * Ini menerima objek produk lengkap dari hasil API (misalnya dari scan barcode).
         * @param {Object} productToAdd - Objek produk lengkap dari API (misalnya {id, name, price, stock, image, ...}).
         * @param {number} quantityToAdd - Kuantitas yang ingin ditambahkan (default 1).
         */
        addToCart(productToAdd, quantityToAdd = 1) {
            // Validasi dasar: pastikan productToAdd adalah objek dan memiliki ID serta stok
            if (!productToAdd || typeof productToAdd.id === 'undefined' || typeof productToAdd.stock === 'undefined') {
                console.error("Invalid product object provided to addToCart:", productToAdd);
                alert("Produk tidak valid untuk ditambahkan ke keranjang.");
                return;
            }

            const existingItem = this.items.find(item => item.id === productToAdd.id);
            const productPrice = parseFloat(productToAdd.price);

            if (isNaN(productPrice)) {
                console.error(`Invalid price for product ${productToAdd.name}: ${productToAdd.price}`);
                alert("Harga produk tidak valid.");
                return;
            }

            if (existingItem) {
                // Jika produk sudah ada, tambahkan kuantitasnya
                if (existingItem.quantity + quantityToAdd <= productToAdd.stock) {
                    existingItem.quantity += quantityToAdd;
                    console.log(`Increased quantity for "${productToAdd.name}". New quantity: ${existingItem.quantity}`);
                } else {
                    alert(`Stok ${productToAdd.name} hanya ${productToAdd.stock}, tidak bisa menambah lebih banyak.`);
                    return;
                }
            } else {
                // Jika produk belum ada, tambahkan sebagai item baru ke keranjang
                if (quantityToAdd <= productToAdd.stock) {
                    // Simpan semua detail produk yang relevan langsung di item keranjang
                    this.items.push({
                        id: productToAdd.id,
                        name: productToAdd.name,
                        price: productPrice, // Gunakan harga yang sudah dikonversi
                        quantity: quantityToAdd,
                        stock: productToAdd.stock, // Simpan stok produk untuk validasi di kemudian hari
                        image: productToAdd.image, // Simpan URL gambar
                        // Anda bisa menambahkan properti lain dari productToAdd di sini jika diperlukan di keranjang/checkout
                        category: productToAdd.category,
                        sub_category: productToAdd.sub_category,
                        category_name: productToAdd.category_name,
                        sub_category_name: productToAdd.sub_category_name,
                    });
                    console.log(`Added new product "${productToAdd.name}" to cart.`);
                } else {
                    alert(`Stok ${productToAdd.name} hanya ${productToAdd.stock}, tidak bisa menambah lebih banyak.`);
                    return;
                }
            }
            this.saveCart(); // Simpan perubahan ke localStorage
        },

        /**
         * Mengurangi kuantitas produk di keranjang atau menghapusnya jika kuantitas menjadi 0.
         * @param {number} productId - ID produk yang akan dihapus/dikurangi dari keranjang.
         * @param {number} change - Jumlah perubahan kuantitas (misal -1 untuk mengurangi).
         */
        updateQuantity(productId, change) {
            const item = this.items.find(item => item.id === productId);

            if (item) {
                const newQuantity = item.quantity + change;
                // Validasi terhadap stok yang disimpan di item keranjang
                if (newQuantity > 0 && newQuantity <= item.stock) { 
                    item.quantity = newQuantity;
                    console.log(`Updated quantity for product ID ${productId}. New quantity: ${item.quantity}`);
                } else if (newQuantity <= 0) {
                    this.removeFromCart(productId); // Hapus jika kuantitas jadi 0 atau kurang
                    console.log(`Removed product ID ${productId} due to quantity <= 0.`);
                } else if (newQuantity > item.stock) {
                    alert(`Stok ${item.name} hanya ${item.stock}, tidak bisa menambah lebih banyak.`);
                }
            } else {
                console.warn(`Attempted to update quantity for product ID ${productId} but it was not found in cart.`);
            }
            this.saveCart(); // Simpan perubahan ke localStorage
        },

        /**
         * Menghapus produk sepenuhnya dari keranjang.
         * @param {number} productId - ID produk yang akan dihapus.
         */
        removeFromCart(productId) {
            this.items = this.items.filter(item => item.id !== productId);
            console.log(`Removed product ID ${productId} from cart.`);
            this.saveCart(); // Simpan perubahan ke localStorage
        },

        /**
         * Mengosongkan seluruh keranjang belanja.
         */
        clearCart() {
            this.items = [];
            console.log('Cart cleared.');
            this.saveCart(); // Simpan perubahan ke localStorage
        },

        // Action untuk menyimpan ke localStorage
        saveCart() {
            if (process.client) { // Hanya berjalan di browser
                localStorage.setItem('cartItems', JSON.stringify(this.items));
            }
        },

        // Action untuk memuat dari localStorage
        loadCart() {
            if (process.client) {
                const storedCart = localStorage.getItem('cartItems');
                if (storedCart) {
                    this.items = JSON.parse(storedCart);
                    console.log('Cart loaded from localStorage.');
                }
            }
        },

        // Tambahkan action checkout yang akan berkomunikasi dengan backend
        async checkout(customerName, paymentMethod, totalAmountPaid) {
            const apiClient = useApiClient(); // Dapatkan instance $fetch untuk panggilan API
            if (this.items.length === 0) {
                console.warn('Keranjang kosong, tidak bisa checkout.');
                return false;
            }

            const orderData = {
                // Asumsi backend Anda mengharapkan user ID dari token JWT
                // Jika tidak, Anda mungkin perlu menambahkan id_user di sini
                customer_name: customerName, // Jika backend Anda punya field customer_name
                payment_method: paymentMethod,
                total_amount: totalAmountPaid,
                items: this.items.map(item => ({
                    product: item.id, // Kirim hanya ID produk
                    quantity: item.quantity,
                    price_at_sale: item.price, // Harga produk saat transaksi
                })),
            };

            try {
                const response = await apiClient('/orders/', { // Ganti dengan endpoint orders Anda
                    method: 'POST',
                    body: orderData,
                });
                this.clearCart(); // Kosongkan keranjang setelah berhasil
                console.log('Pesanan berhasil dibuat:', response);
                return true;
            } catch (error) {
                console.error('Gagal menyelesaikan pesanan:', error.data || error.message);
                // Tambahkan penanganan error yang lebih spesifik jika diperlukan
                alert(`Pembayaran gagal: ${error.data?.detail || error.message}`);
                return false;
            }
        },
    },

    // Plugin Persist Pinia
    persist: {
        storage: process.client ? localStorage : undefined, // Gunakan localStorage di sisi client
        paths: ['items'], // Hanya simpan state 'items'
        key: 'cart-store', // Nama kunci di localStorage, opsional
    },
});
