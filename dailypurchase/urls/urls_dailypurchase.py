from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from ..views import *

urlpatterns=[
    path('category/', CategoryListView.as_view(), name='category'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('payment/', PaymentListView.as_view(), name='payment'),
    path('payment/<int:pk>', PaymentDetailView.as_view(), name='payment_detail'),
    path('dailypurchase/', DailypurchaseListView.as_view(), name='dailypurchase'),
    path('dailypurchase/<int:pk>', DailypurchaseDetailView.as_view(), name='dailypurchase_detail'),
    path('supplier/', SupplierListView.as_view(), name='supplier'),
    path('supplier/<int:pk>', SupplierDetailView.as_view(), name='supplier_detail'),
]
