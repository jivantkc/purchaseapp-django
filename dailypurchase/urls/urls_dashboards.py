from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from ..views import *

urlpatterns=[
    path('dashboards/', DashboardsListView.as_view(), name='dashboards'),
    # path('dashboards/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
]
