from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema

from .models import Cart, CartItem
from .serializers import AlterCartSerializer
from products.models import Product


@api_view(['GET'])
def cart_view(request):
    cart_obj = Cart.objects.new_or_get(request)
    items = cart_obj.items.all()
    total_price = cart_obj.get_total_price()
    return Response({
        "cart_id": cart_obj.id,
        "items": [{"product": item.product.name, "quantity": item.quantity, "total_price": item.get_total_price()} for item in items],
        "total_cart_price": total_price
    })


@extend_schema(request=AlterCartSerializer(), 
               responses={200: {'type': 'object', 'properties': {'message': {'type': 'string'}}}})
@api_view(['POST'])
def add_to_cart_view(request):
    cart_obj = Cart.objects.new_or_get(request)
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    if not product_id:
        return Response({"error": "Product ID is required."}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart_obj, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return Response({"message": f"Added {quantity} of {product.name} to cart."})

@extend_schema(
    request=AlterCartSerializer(),responses={200: {'type': 'object', 'properties': {'message': {'type': 'string'}}}})
@api_view(['POST'])
def remove_from_cart_view(request):
    cart_obj = Cart.objects.new_or_get(request)
    product_id = request.data.get('product_id')

    if not product_id:
        return Response({"error": "Product ID is required."}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)

    try:
        cart_item = CartItem.objects.get(cart=cart_obj, product=product)
        cart_item.quantity -= request.data.get('quantity', 1)
        if cart_item.quantity <= 0:
            cart_item.delete()
        return Response({"message": f"Removed {request.data.get('quantity', 1)} of {product.name} from cart."})
    except CartItem.DoesNotExist:
        return Response({"error": "Product not in cart."}, status=404)
