from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'status', 'created_at', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum([item.quantity * item.price for item in obj.items.all()]) + obj.shipping_price

class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()