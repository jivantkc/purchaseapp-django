from rest_framework import serializers;
from rest_framework.serializers import(
     CharField,
     Serializer,
     )
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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"
        

class SupplierSerializer(serializers.ModelSerializer):
    category_name= serializers.ReadOnlyField(source='category.name')

    class Meta:
        model=Supplier
        fields="__all__"


class DailypurchaseSerializer(serializers.ModelSerializer):
    suppliers= serializers.CharField(source='suppliers.name')
    category= serializers.CharField(source='category.name')
    payment= serializers.CharField(source='payment.name')
    class Meta:
        model=Dailypurchase
        fields="__all__"

    def create(self, validated_data):
        mydict={}
        myfields=['suppliers','category','payment']

        for e in myfields: 
            mydict[e]=validated_data.pop(e)['name']


        '''
        Serialising foreign keys suppliers
        '''
        suppliers_data=Supplier.objects.filter(name=mydict["suppliers"])
        category_data=Category.objects.filter(name=mydict["category"])
        payment_data=Payment.objects.filter(name=mydict["payment"])
        updatedMydict={'suppliers':suppliers_data[0],'category':category_data[0],'payment':payment_data[0]}
        '''
        Serialising foreign keys category
        '''
        validated_data.update(updatedMydict)
        # print(validated_data)
        return Dailypurchase.objects.create(**validated_data)
      