from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from .models import Product
from .serializers import ProductSerializer

@extend_schema(operation_id="products_list")
@api_view(['GET'])
def product_list_view(request):
    serializer = ProductSerializer(data=list(Product.objects.all()), many=True)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@extend_schema(operation_id="product_detail")
@api_view(['GET'])
def product_detail_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)