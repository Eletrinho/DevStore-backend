from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from .models import Product

@extend_schema(operation_id="products_list")
@api_view(['GET'])
def product_list_view(request):
    products = Product.objects.all()
    product_data = [{"id": product.id, "name": product.name, "price": product.price} for product in products]
    return Response(product_data)

@extend_schema(operation_id="product_detail")
@api_view(['GET'])
def product_detail_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product_data = {"id": product.id, "name": product.name, "price": product.price}
        return Response(product_data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)