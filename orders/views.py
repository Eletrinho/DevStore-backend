from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_spectacular.utils import extend_schema

from .serializers import OrderSerializer, CheckoutSerializer
from .models import Order, OrderItem
from cart.models import Cart
from users.models import Address


@extend_schema(request=CheckoutSerializer, responses={200: OrderSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def checkout_view(request):
    cart_obj = Cart.objects.new_or_get(request)
    if not cart_obj.items.exists():
        return Response({"error": "Cart is empty."}, status=400)

    address_id = request.data.get('address_id')
    if not address_id:
        return Response({"error": "Address ID is required."}, status=400)

    address = get_object_or_404(Address, id=address_id, user=request.user)
    serializer = OrderSerializer(
        data={'user': request.user.id, 'address': address.id})

    items = cart_obj.items.all()
    if any(item.product.stock < item.quantity for item in items):
        return Response({"error": "Not enough stock for one or more products."}, status=400)
    serializer.is_valid(raise_exception=True)
    total = 0
    order = serializer.save()

    for item in cart_obj.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        total += item.quantity * item.product.price
        item.product.stock -= item.quantity
        item.product.save()
    order.total_price = total + order.shipping_price
    order.save()
    cart_obj.items.all().delete()
    return Response({"message": "Checkout successful!", "order_id": serializer.instance.id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_data = []
    for order in orders:
        items = order.items.all()
        order_data.append({
            "order_id": order.id,
            "created_at": order.created_at,
            "status": order.status,
            "items": [{"product": item.product.name, "quantity": item.quantity, "price": item.price} for item in items],
            "total_price": order.total_price
        })
    return Response(order_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        items = order.items.all()
        order_data = {
            "order_id": order.id,
            "status": order.status,
            "created_at": order.created_at,
            "items": [{"product": item.product.name, "quantity": item.quantity, "price": item.price} for item in items],
            "total_price": order.total_price
        }
        return Response(order_data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        if order.status != 'created':
            return Response({"error": "Only created orders can be cancelled."}, status=400)
        order.status = 'cancelled'
        order.save()
        return Response({"message": "Order cancelled successfully."})
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=404)
