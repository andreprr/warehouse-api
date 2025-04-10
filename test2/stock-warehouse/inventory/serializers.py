from rest_framework import serializers
from .models import PurchaseHeader, PurchaseDetail, Item, SellHeader, SellDetail

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('stock', 'balance', 'created_at', 'updated_at', 'is_deleted')

class PurchaseHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHeader
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_deleted')


class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_deleted')

    def validate(self, data):
        if data['quantity'] <= 0 or data['unit_price'] <= 0:
            raise serializers.ValidationError("Quantity and unit_price must be greater than 0.")
        return data

from .models import SellHeader, SellDetail

class SellHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellHeader
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_deleted')


class SellDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetail
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_deleted')

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return data
