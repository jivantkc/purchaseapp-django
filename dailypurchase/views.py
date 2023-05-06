from .models import *
from .serializers import (CategorySerializer,
                          DailypurchaseSerializer,
                          PaymentSerializer,
                          SupplierSerializer,
                          UserSerializer,
                          UserSerializerWithToken,
                          MyTokenObtainPairSerialiser,
                          ChangePasswordSerializer,
                         )
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from django.http.response import JsonResponse



"""
Authentication Token Generator"""
 
class MyTokenObtainPairView(TokenObtainPairView):
     serializer_class=MyTokenObtainPairSerialiser
     
"""
User Registration View
"""

class UserRegistrationView(APIView):
    def post(self, request,format=None):
        data=request.data  
        try:
             user=User.objects.create(
                  first_name=data["name"],
                  username=data["email"],
                  email=data["email"],
                  password=make_password(data["password"])
             )
             serializer=UserSerializerWithToken(user, many=False)
             return Response(serializer.data)
        except:
             if data=={}:
                    return Response("Please Input all data", status=status.HTTP_400_BAD_REQUEST)
             else:
                
                message={"detail":"User with this email already exists"}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
             
         
"""
Change password
"""
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Create your views here.
class ProfileListView(APIView):
    permission_classes =([IsAuthenticated,])
    def get(self, request,format=None):
        query=request.user
        serializer=UserSerializer(query, many=False)
        return Response(serializer.data)
        # return Response("Is Authenticated by token")


class CategoryListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,format=None):
        category=Category.objects.filter(user=request.user)
        serializer=CategorySerializer(category, many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
         serializer=CategorySerializer(data=request.data)
         if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=CategorySerializer(model)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=CategorySerializer(model, request.data)
            if serializer.is_valid():
                 serializer.save
                 return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = CategorySerializer(transformer,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  


    def delete(self, request, pk, format=None):
            model=self.get_object(pk)
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)



class PaymentListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,format=None):
        model=Payment.objects.filter(user=request.user)
        serializer=PaymentSerializer(model, many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
         serializer=PaymentSerializer(data=request.data)
         if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PaymentDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=PaymentSerializer(model)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
            modeli=self.get_object(pk)
            # serializer=PaymentSerializer(model, request.data)
            serializer=PaymentSerializer(modeli, data=request.data)
            if serializer.is_valid():
                 serializer.save
                 return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = PaymentSerializer(transformer,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  

    def delete(self, request, pk, format=None):
            model=self.get_object(pk)
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)





class SupplierListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,format=None):
        model=Supplier.objects.filter(user=request.user)
        serializer=SupplierSerializer(model, many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
         serializer=SupplierSerializer(data=request.data)
         if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SupplierDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=SupplierSerializer(model)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=SupplierSerializer(model, request.data)
            if serializer.is_valid():
                 serializer.save
                 return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk, format=None):
            model=self.get_object(pk)
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)



class DailypurchaseListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,format=None):
        model=Dailypurchase.objects.filter(user=request.user)
        serializer=DailypurchaseSerializer(model, many=True)
        # print(serializer.data)
        return Response(serializer.data)
    
 
    def post(self,request,format=None):
        serializer=DailypurchaseSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DailypurchaseDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Dailypurchase.objects.get(pk=pk)
        except Dailypurchase.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=DailypurchaseSerializer(model)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=DailypurchaseSerializer(model, request.data)
            if serializer.is_valid():
                 serializer.save
                 return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = DailypurchaseSerializer(transformer,
                                           data=request.data,
                                           partial=True)
        
 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  


    def delete(self, request, pk, format=None):
            model=self.get_object(pk)
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


