from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Item,  SellHeader, SellDetail
from .serializers import ItemSerializer, SellHeaderSerializer, SellDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from datetime import datetime


class ItemViewSet(viewsets.ViewSet):
    def list(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, code=None):
        item = get_object_or_404(Item.objects, code=code)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, code=None):
        item = get_object_or_404(Item.objects, code=code)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, code=None):
        item = get_object_or_404(Item.objects, code=code)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from .models import PurchaseHeader, PurchaseDetail
from .serializers import PurchaseHeaderSerializer, PurchaseDetailSerializer


class PurchaseHeaderViewSet(viewsets.ViewSet):
    def list(self, request):
        purchases = PurchaseHeader.objects.all()
        serializer = PurchaseHeaderSerializer(purchases, many=True)
        return Response(serializer.data)

    def retrieve(self, request, code=None):
        purchase = get_object_or_404(PurchaseHeader.objects, code=code)
        serializer = PurchaseHeaderSerializer(purchase)
        return Response(serializer.data)

    def create(self, request):
        serializer = PurchaseHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseDetailViewSet(viewsets.ViewSet):
    def list(self, request, header_code=None):
        details = PurchaseDetail.objects.filter(header__code=header_code)
        serializer = PurchaseDetailSerializer(details, many=True)
        return Response(serializer.data)

    def create(self, request, header_code=None):
        header = get_object_or_404(PurchaseHeader.objects, code=header_code)
        data = request.data.copy()
        data['header'] = header.id

        serializer = PurchaseDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellHeaderViewSet(viewsets.ViewSet):
    def list(self, request):
        sells = SellHeader.objects.all()
        serializer = SellHeaderSerializer(sells, many=True)
        return Response(serializer.data)

    def retrieve(self, request, code=None):
        sell = get_object_or_404(SellHeader.objects, code=code)
        serializer = SellHeaderSerializer(sell)
        return Response(serializer.data)

    def create(self, request):
        serializer = SellHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellDetailViewSet(viewsets.ViewSet):
    def list(self, request, header_code=None):
        details = SellDetail.objects.filter(header__code=header_code)
        serializer = SellDetailSerializer(details, many=True)
        return Response(serializer.data)

    def create(self, request, header_code=None):
        header = get_object_or_404(SellHeader.objects, code=header_code)
        data = request.data.copy()
        data['header'] = header.id

        serializer = SellDetailSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def stock_report(request, item_code):
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    if not start_date_str or not end_date_str:
        return Response({"error": "start_date and end_date are required."}, status=400)

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    item = get_object_or_404(Item.all_objects, code=item_code)

    # Ambil semua transaksi dalam range
    purchases = PurchaseDetail.objects.filter(
        item=item, 
        header__date__range=(start_date, end_date),
        is_deleted=False
    ).select_related('header').order_by('header__date')

    sells = SellDetail.objects.filter(
        item=item, 
        header__date__range=(start_date, end_date),
        is_deleted=False
    ).select_related('header').order_by('header__date')

    # Gabungkan dan urutkan semua transaksi
    transactions = []

    for p in purchases:
        transactions.append({
            "date": p.header.date,
            "type": "purchase",
            "code": p.header.code,
            "description": p.header.description,
            "qty_in": p.quantity,
            "price_in": p.unit_price,
            "total_in": p.quantity * p.unit_price,
            "qty_out": 0,
            "price_out": 0,
            "total_out": 0
        })

    # Untuk FIFO, kita simpan riwayat pembelian
    fifo_stack = []
    for p in purchases:
        fifo_stack.append({
            "qty": p.quantity,
            "unit_price": p.unit_price
        })

    for s in sells:
        qty = s.quantity
        out_logs = []
        total_out = 0

        # Ambil dari FIFO stack
        while qty > 0 and fifo_stack:
            batch = fifo_stack[0]
            take = min(qty, batch["qty"])
            total_out += take * batch["unit_price"]
            out_logs.append({
                "qty": take,
                "unit_price": batch["unit_price"]
            })
            batch["qty"] -= take
            qty -= take
            if batch["qty"] == 0:
                fifo_stack.pop(0)

        # Boleh breakdown jadi dua baris jika item diambil dari dua batch pembelian
        for ol in out_logs:
            transactions.append({
                "date": s.header.date,
                "type": "sell",
                "code": s.header.code,
                "description": s.header.description,
                "qty_in": 0,
                "price_in": 0,
                "total_in": 0,
                "qty_out": ol["qty"],
                "price_out": ol["unit_price"],
                "total_out": ol["qty"] * ol["unit_price"],
            })

    # Urutkan berdasarkan tanggal
    transactions.sort(key=lambda x: x["date"])

    # Hitung balance berjalan
    current_stock = 0
    current_balance = 0
    history = []

    for tx in transactions:
        if tx["qty_in"]:
            current_stock += tx["qty_in"]
            current_balance += tx["total_in"]
        elif tx["qty_out"]:
            current_stock -= tx["qty_out"]
            current_balance -= tx["total_out"]

        tx["running_stock"] = current_stock
        tx["running_balance"] = current_balance
        history.append(tx)

    return Response({
        "item": {
            "code": item.code,
            "name": item.name,
            "unit": item.unit,
            "description": item.description,
        },
        "transactions": history,
        "summary": {
            "final_stock": current_stock,
            "final_balance": current_balance
        }
    })