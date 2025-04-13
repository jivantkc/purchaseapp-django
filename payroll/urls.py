from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import *

urlpatterns=[
    path('fixedexpense/', FixedExpenseListView.as_view(), name='fixedexpense'),
    path('fixedexpense/<int:pk>/', FixedExpenseDetailView.as_view(), name='fixedexpense_detail'),
    path('otherexpcategory/', OtherExpCategoryListView.as_view(), name='otherexpcategory'),
    path('otherexpcategory/<int:pk>/', OtherExpCategoryDetailView.as_view(), name='otherexpcategory_detail'),
    path('creditors/', CreditorsListView.as_view(), name='creditors'),
    path('creditors/<int:pk>/', CreditorsDetailView.as_view(), name='creditors_detail'),
  
]
