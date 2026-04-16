from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema

from .models import Address
from .serializers import UserSerializer, RegisterSerializer, AddressSerializer

@extend_schema(request=RegisterSerializer(), responses={201: UserSerializer})
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": f"Registrado com sucesso! {serializer.data['full_name']}."}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def user_detail_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@extend_schema(request=UserSerializer(), responses={200: UserSerializer})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update_view(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.auth.delete()
    return Response({"message": "Logout realizado com sucesso."}, status=200)

@extend_schema(request=AddressSerializer(), responses={201: AddressSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def address_create_view(request):
    serializer = AddressSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def address_list_view(request):
    addresses = request.user.addresses.all()
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def address_update_view(request, address_id):
    try:
        address = request.user.addresses.get(id=address_id)
    except Address.DoesNotExist:
        return Response({"error": "Address not found."}, status=404)
    
    serializer = AddressSerializer(address, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)