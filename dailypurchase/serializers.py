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
        fields=["id","username","email", "token", "is_staff"]
    
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
    category_name= serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model=Supplier
        fields = ['id', 'user','name', 'category','category_name']


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
        return Dailypurchase.objects.create(**validated_data)
      
    
    def update(self, instance, validated_data):
        '''
        Updating foreign keys category
        '''
        instance.date = validated_data.get('date', instance.date)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.purchase = validated_data.get('purchase', instance.purchase)

        # Get the supplier instance
        suppliers_data=validated_data.pop("suppliers")
        supplier=Supplier.objects.get(name=suppliers_data["name"],user=instance.user)
        # Update the dailypurchase instance with the supplier instance
        instance.suppliers = supplier

        # Get the category instance
        category_data=validated_data.pop("category")
        category=Category.objects.get(name=category_data["name"],user=instance.user)
        # Update the dailypurchase instance with the supplier instance
        instance.category = category

        # Get the category instance
        payment_data=validated_data.pop("payment")
        print(payment_data["name"])
        payment=Payment.objects.get(name=payment_data["name"], user=instance.user)
        # Update the dailypurchase instance with the supplier instance
        instance.payment = payment

        instance.save()
        return instance
      
    