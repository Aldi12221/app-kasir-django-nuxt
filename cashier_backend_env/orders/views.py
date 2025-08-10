# cashier_backend/orders/views.py

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum, F
from datetime import date, datetime, time
from django.utils import timezone
from django.db import transaction # Penting untuk atomicity
from django.db.models import Sum, Count # Diperlukan untuk daily_summary
from django.utils import timezone # Diperlukan untuk daily_summary
from datetime import timedelta # Diperlukan untuk daily_summary
from cashier_backend.permissions import IsAdminUser, IsCashierOrAdmin, IsOwnerOrAdmin 



from .serializers import OrderSerializer, OrderItemSerializer, CashierRegistrationSerializer,User
from .models import Order, OrderItem
from products.models import Product # Import model Product
from decimal import Decimal # Import Decimal untuk akurasi harga



from rest_framework import mixins, generics # Import ini
# Import serializer baru
 
# Import permission yang sudah kita buat


# Jika Anda menggunakan otentikasi (seperti JWT atau Session)
# from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all().order_by('-created_at')
    serializer_class = OrderSerializer
    # Jika Anda memerlukan otentikasi, aktifkan baris ini:
    # permission_classes = [IsAuthenticated] 

    def get_permissions(self):
        # ... (print statements) ...

        # Jika Anda tidak memakai shortcut admin di atas:
        if self.action in ['list', 'retrieve', 'today_orders', 'daily_summary','categories']: # <-- TAMBAHKAN 'daily_summary' DI SINI
            permission_classes = [IsAuthenticated, IsCashierOrAdmin]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsCashierOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else: # Ini adalah fallback, sebaiknya hindari jika semua action perlu izin spesifik
            permission_classes = [IsAuthenticated] 
        return [permission() for permission in permission_classes]


    @action(detail=False, methods=['post'], url_path='process_checkout')
    def process_checkout(self, request):
        data = request.data
        items_data = data.get('items', [])
        total_amount = data.get('total_amount')
        payment_method = data.get('payment_method')

        if not items_data:
            return Response(
                {"error": "Keranjang kosong. Tidak ada item untuk diproses."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if total_amount is None or not payment_method: # Pengecekan None untuk total_amount
             return Response(
                {"error": "Total amount dan payment method wajib."},
                status=status.HTTP_400_BAD_REQUEST
             )
        
        try:
            # Pastikan total_amount dikonversi ke Decimal dengan aman
            total_amount_decimal = Decimal(str(total_amount)) 
        except Exception:
            return Response(
                {"error": "Total amount tidak valid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic(): # Pastikan semua operasi database atomik
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None, # Sesuaikan jika user opsional
                    total_amount=total_amount_decimal, # Gunakan Decimal yang sudah dikonversi
                    payment_method=payment_method,
                    status='pending', # Pastikan field 'status' ada di model Order Anda dan diset default
                )

                for item_data in items_data:
                    product_id = item_data.get('product')
                    quantity = item_data.get('quantity')
                    price_at_purchase = item_data.get('price_at_purchase')

                    if not product_id or not quantity or not price_at_purchase:
                        raise Exception("Data item pesanan tidak lengkap.")

                    try:
                        # Pastikan price_at_purchase dikonversi ke Decimal dengan aman
                        price_at_purchase_decimal = Decimal(str(price_at_purchase))
                    except Exception:
                        raise Exception(f"Harga pembelian untuk produk {product_id} tidak valid.")

                    try:
                        product = Product.objects.select_for_update().get(id=product_id)
                    except Product.DoesNotExist:
                        raise Exception(f"Produk dengan ID {product_id} tidak ditemukan.")

                    if product.stock < quantity:
                        raise Exception(f"Stok tidak cukup untuk {product.name}. Tersedia: {product.stock}, Diminta: {quantity}")

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price_at_purchase=price_at_purchase_decimal
                    )

                    product.stock -= quantity
                    product.save()

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    # ---
    
    # ## **`daily_summary` Action**
    
    # Ini adalah action yang akan melayani permintaan GET ke `/api/orders/daily_summary/`.

    # ```python
    @action(detail=False, methods=['get'], url_path='daily_summary')
    def daily_summary(self, request):
        today = timezone.now().date()
        # Menggunakan timezone.make_aware() untuk memastikan datetime aware
        start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

        today_orders = Order.objects.filter(
            created_at__gte=start_of_day,
            created_at__lte=end_of_day
        )

        total_revenue = today_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_transactions = today_orders.count()
        
        # Contoh mendapatkan top selling products (opsional, bisa diaktifkan)
        # top_selling_items = OrderItem.objects.filter(
        #     order__in=today_orders
        # ).values('product__name').annotate(
        #     total_quantity=Sum('quantity')
        # ).order_by('-total_quantity')[:5]

        return Response({
            'date': today.isoformat(),
            'total_revenue': total_revenue,
            'total_transactions': total_transactions,
            # 'top_selling_items': list(top_selling_items), # Uncomment jika diaktifkan
        }, status=status.HTTP_200_OK)
        
class CashierRegistrationView(generics.CreateAPIView):
   
    
    queryset = User.objects.all() # Queryset dasar, tidak terlalu penting untuk CreateAPIView
    serializer_class = CashierRegistrationSerializer
    permission_classes = [IsAdminUser] 

    # ---
    
    # ## **`daily_summary` Action**
    
    # Ini adalah action yang akan melayani permintaan GET ke `/api/orders/daily_summary/`.

    # ```python

class DailySummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        today = date.today()
        
        # Default ke tanggal hari ini jika parameter tidak disediakan atau tidak valid
        try:
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            else:
                start_date = today
        except ValueError:
            return Response({"error": "Invalid start_date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            else:
                end_date = today
        except ValueError:
            return Response({"error": "Invalid end_date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Pastikan tanggal akhir tidak lebih awal dari tanggal mulai
        if start_date > end_date:
            return Response({"error": "start_date cannot be after end_date."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter order berdasarkan tanggal pembuatan (created_at atau order_date)
        # Asumsi: model Order Anda memiliki field 'created_at' atau 'order_date'
        # yang merupakan DateTimeField atau DateField
        orders_in_range = Order.objects.filter(
            created_at__date__gte=start_date, # Filter dari tanggal mulai (inklusif)
            created_at__date__lte=end_date    # Filter sampai tanggal akhir (inklusif)
        )
        
        # Hitung total revenue dari orders_in_range
        # Asumsi Order memiliki field 'total_amount'
        total_revenue = orders_in_range.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Hitung total transaksi (jumlah order)
        total_transactions = orders_in_range.count()

        data = {
            'total_revenue': total_revenue,
            'total_transactions': total_transactions,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }
        return Response(data, status=status.HTTP_200_OK)
    