from rest_framework import serializers;
from rest_framework.serializers import(
     CharField,
     Serializer,
     )
from .models import (Creditors,OtherExpCategory,FixedExpense)
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

 

"""
PAYROLL SERIALIZERS
"""
class CreditorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Creditors
        fields="__all__"


class OtherExpCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=OtherExpCategory
        fields="__all__"
        

 

class FixedExpenseSerializer(serializers.ModelSerializer):
    creditors= serializers.CharField(source='creditors.name')
    category= serializers.CharField(source='category.name')
    
    class Meta:
        model=FixedExpense
        fields="__all__"

    def create(self, validated_data):
        mydict={}
        myfields=['creditors','category']

        for e in myfields: 
            mydict[e]=validated_data.pop(e)['name']


        '''
        Serialising foreign keys creditors
        '''
        creditors_data=Creditors.objects.filter(name=mydict["creditors"])
        category_data=OtherExpCategory.objects.filter(name=mydict["category"])
        
        updatedMydict={'creditors':creditors_data[0],'category':category_data[0]}
        '''
        Serialising foreign keys category
        '''
        validated_data.update(updatedMydict)
        return FixedExpense.objects.create(**validated_data)
      
    
    def update(self, instance, validated_data):
        '''
        Updating foreign keys category
        '''
        instance.date = validated_data.get('date', instance.date)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.expensedetails = validated_data.get('expensedetails', instance.expensedetails)
       

        # Get the Creditors instance
        creditors_data=validated_data.pop("creditors")
        creditors=Creditors.objects.get(name=creditors_data["name"],user=instance.user)
        # Update the Otherexpense instance with the creditors instance
        instance.creditors = creditors

        # Get the expensecategory instance
        category_data=validated_data.pop("category")
        category=OtherExpCategory.objects.get(name=category_data["name"],user=instance.user)
        # Update the dailypurchase instance with the supplier instance
        instance.category = category

        instance.save()
        return instance
      
    