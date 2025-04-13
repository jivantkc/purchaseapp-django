from .models import *
from .serializers import (CreditorsSerializer,
                          OtherExpCategorySerializer,
                          FixedExpenseSerializer,
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

 
class CreditorsListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,format=None):
        creditors=Creditors.objects.filter(user=request.user)
        serializer=CreditorsSerializer(creditors, many=True)
        return Response(serializer.data)
    
       
        
    
    def post(self,request,format=None):
         request.data['user'] = request.user.id
         serializer=CategorySerializer(data=request.data)
         if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CreditorsDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Creditors.objects.get(pk=pk)
        except Creditors.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=CreditorsSerializer(model)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=CreditorsSerializer(model, request.data)
            if serializer.is_valid():
                 serializer.save
                 return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = CreditorsSerializer(transformer,
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



class OtherExpCategoryListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,format=None):
        model=OtherExpCategory.objects.filter(user=request.user)
        serializer=OtherExpCategorySerializer(model, many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
         request.data['user'] = request.user.id
         serializer=OtherExpCategorySerializer(data=request.data)
         if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class OtherExpCategoryDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return OtherExpCategory.objects.get(pk=pk)
        except OtherExpCategory.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=OtherExpCategorySerializer(model)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
            modeli=self.get_object(pk)
            # serializer=OtherExpCategorySerializer(model, request.data)
            serializer=OtherExpCategorySerializer(modeli, data=request.data)
            if serializer.is_valid():
                 serializer.save
                 return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = OtherExpCategorySerializer(transformer,
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


class FixedExpenseListView(APIView):
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

        queryset = FixedExpense.objects.filter(user=request.user, date__range=[first_day, last_day]).order_by('-id')
        
        # print(queryset)

        #get data for dashboard
        # Group by category and annotate
        # Group by category and annotate
        # dashboard = queryset.values(
        #     'category__name'
        # ).annotate(
            
        #     # total_quantity=Sum('quantity'),
        #     total=Sum('amount')
        # ).order_by('-total')
        
        
        # Get pagination parameters from request
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 3)
    
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
    
        serializer=FixedExpenseSerializer(page_obj, many=True)
         
    
        return Response({
        'data': serializer.data,
     
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
        serializer = FixedExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FixedExpenseDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return FixedExpense.objects.get(pk=pk)
        except FixedExpense.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=FixedExpenseSerializer(model)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
            model=self.get_object(pk)
            serializer=FixedExpenseSerializer(model, request.data)
            if serializer.is_valid():
                 serializer.save
                 return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = FixedExpenseSerializer(transformer,
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


