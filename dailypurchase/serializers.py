from rest_framework import serializers;
from .models import (Category,Dailypurchase,Payment,Supplier)
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

"""
Step One
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email"]


"""
Step2 
"""
class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields=["id","username","email", "token"]
    
    def get_token(self, obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)

"""
Step3 
"""
class MyTokenObtainPairSerialiser(TokenObtainPairSerializer):
    def validate(self, attrs):
        data=super().validate(attrs)
        serializers=UserSerializerWithToken(self.user).data

        for k,v in serializers.items():
            data[k]=v
        return data

"""
ChangePassword
"""

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


"""
APP SERIALIZERS
"""
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class DailypurchaseSerializer(serializers.ModelSerializer):
    suppliers= serializers.ReadOnlyField(source='suppliers.name')
    category= serializers.ReadOnlyField(source='category.name')
    payment= serializers.ReadOnlyField(source='payment.name')
    class Meta:
        model=Dailypurchase
        fields="__all__"
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"
        

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields="__all__"
        
