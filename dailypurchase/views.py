from .models import *
from payroll.models import *
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
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.utils import timezone
from rest_framework.response import Response
from django.db.models import Sum, Q

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
         request.data['user'] = request.user.id
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
         request.data['user'] = request.user.id
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
         request.data['user'] = request.user.id
        #  user=self.request.user
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
    
    def patch(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = SupplierSerializer(transformer,
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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page'
    max_page_size = 10


class DailypurchaseListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,format=None):
        now = timezone.now()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Calculate last day of month
        if now.month == 12:
            last_day = now.replace(year=now.year+1, month=1, day=1)
        else:
            last_day = now.replace(month=now.month+1, day=1)
        last_day = last_day - timezone.timedelta(days=1)

        queryset = Dailypurchase.objects.filter(user=request.user, date__range=[first_day, last_day]).order_by('-id')
        
        # print(queryset)

        #get data for dashboard
        # Group by category and annotate
        # Group by category and annotate
        dashboard = queryset.values(
            'category__name'
        ).annotate(
            
            # total_quantity=Sum('quantity'),
            total=Sum('amount')
        ).order_by('-total')
        
        
        # Get pagination parameters from request
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 3)
    
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
    
        serializer=DailypurchaseSerializer(page_obj, many=True)
         
    
        return Response({
        'data': serializer.data,
        'dashboard':dashboard,
        'total': paginator.count,
        'page': page_obj.number,
        'per_page': int(per_page),
        'total_pages': paginator.num_pages,
        })

    
 
    def post(self,request,format=None):
        # Add the authenticated user to the request data
        request.data['user'] = request.user.id  # Ensure the user is associated with the purchase
        # print("Received!", request.data)

        # Validate and save the data
        serializer = DailypurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle validation errors
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



class DashboardsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,format=None):
        now = timezone.now()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Calculate last day of month
        if now.month == 12:
            last_day = now.replace(year=now.year+1, month=1, day=1)
        else:
            last_day = now.replace(month=now.month+1, day=1)
        last_day = last_day - timezone.timedelta(days=1)

        queryset1 = Dailypurchase.objects.filter(user=request.user, date__range=[first_day, last_day]).order_by('-id')
        queryset2 = FixedExpense.objects.filter(user=request.user, date__range=[first_day, last_day]).order_by('-id')
        
        # print(queryset)

        #get data for dashboard
        # Group by category and annotate
        # Group by category and annotate
        dashboard1 = queryset1.values(
            'category__name'
        ).annotate(
            
            # total_quantity=Sum('quantity'),
            total=Sum('amount')
        ).order_by('-total')

        dashboard2 = queryset2.values(
            'category__name'
        ).annotate(
            
            # total_quantity=Sum('quantity'),
            total=Sum('amount')
        ).order_by('-total')
        
        dashboard = [*dashboard1, *dashboard2]
        dashboard = sorted(dashboard, key=lambda x: x['total'], reverse=True)
        
        return Response({
        'data': dashboard,
        })

    
 
    def post(self,request,format=None):
        # Add the authenticated user to the request data
        request.data['user'] = request.user.id  # Ensure the user is associated with the purchase
        # print("Received!", request.data)

        # Validate and save the data
        serializer = DailypurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
