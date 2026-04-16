from rest_framework import serializers
from .models import User, Address

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'full_name', 'phone', 'created_at')

        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'phone': {'read_only': True},
        }
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'full_name', 'phone', 'created_at')

        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
        }
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'street', 'city', 'state', 'zip_code', 'country')
        extra_kwargs = {
            'user': {'read_only': True},
        }