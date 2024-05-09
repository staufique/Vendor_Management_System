from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code', 'email']

    def validate_email(self, value):
        if not "@" in value:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'context' in kwargs and 'request' in kwargs['context'] and kwargs['context']['request'].method == 'GET':
            self.Meta.fields = '__all__'

    

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['vendor','items','quality_rating']

    def validate_quality_rating(self, value):
        if value > 5.0 or value < 0.0:
            raise serializers.ValidationError("quality rating must be greater than 0 or less than or equal to 5")
        return value
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'context' in kwargs and 'request' in kwargs['context'] and kwargs['context']['request'].method == 'GET':
            self.Meta.fields = '__all__'


class UserSigunUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Username must be at least 5 characters long.")
        return value

    def validate_email(self, value):
        if not "@" in value:
            raise serializers.ValidationError("Invalid email format.")
        return value
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']