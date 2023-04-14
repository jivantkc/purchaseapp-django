from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from ..views import ProfileListView, MyTokenObtainPairView,UserRegistrationView,ChangePasswordView

"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers import UserSerializerWithToken


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serialiser=UserSerializerWithToken(self.user).data
        for k,v in serialiser.items():
              data[k]=v
        return data
       
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
"""



urlpatterns=[
  path('register/', UserRegistrationView.as_view(), name='user_registration'),
  path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('change-password/', ChangePasswordView.as_view(), name='change-password'),
  path('reset-password/', include('django_rest_passwordreset.urls', namespace='reset_password')),
  path('profile/', ProfileListView.as_view(), name='userprofile'),
  ]
