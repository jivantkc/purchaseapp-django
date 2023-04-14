## Create django, django-restframwork, jwt, API depoy in Heroku.
Backend Project created using django.

## STEP1 Virtual Environment
Create a project folder:`mkdir project`

Go to folder:`cd project`

Creating Virtual environment to isolate packages:`python3 -m venv env`

Activate Virtual environment:`source env/bin/activate`

## STEP2 Install Django, project & app
NOTE:This tutorial is created using django 4.1, other dependencies might required for newer versions.

Intall Django:`pip install Django==4.1`

Create Django project:`django-admin startproject api`

Go inside Project folder:`cd api`

Start App:`django-admin startapp myapp`

### Add App to project

go to settings.py then in 

INSTALLED_APPS = [] add following.

     'myapp.apps.MyappConfig',

Run Project:`python manage.py runserver`

This should open up browser in local host and show 

"The install worked successfully! Congratulations!".


## STEP3 Connecting to database.
Use default sqlite or others

#### Setting up ENviron
`pip install django-environ`

In Settings.py:

           import os
           from pathlib import Path
           from datetime import timedelta
           import environ

           env = environ.Env()
           # reading .env file
           environ.Env.read_env()


create .env file in project main folder

     DB_NAME=fill correct info

     DB_USER=fill correct info

     DB_PASSWORD=fill correct info

     DB_HOST=fill correct info
 

Need to install different sql drivers based on your database preference.


#### Mysql
`pip install pymysql`

Edit  __init__.py in project origin and add following 2 lines

     import pymysql

     pymysql.install_as_MySQLdb()


#### In Settings.py:


               DATABASES = {

                   'default': {

                       'ENGINE': 'django.db.backends.mysql',

                       'NAME':env("DB_NAME"),

                       'USER':env("DB_USER"),

                       'PASSWORD':env("DB_PASSWORD"),

                       'HOST':env("DB_HOST"),

                       'PORT':"3306",

                       'OPTIONS':{'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
                   }

               }



#### POSTGRESSQL
`pip3 install psycopg2`


     DATABASES = {
         'default': {

             'ENGINE': 'django.db.backends.postgresql',

             'NAME':env("DB_NAME"),

             'USER':env("DB_USER"),

             'PASSWORD':env("DB_PASSWORD"),

             'HOST':env("DB_HOST"),

             'PORT':'5432',


         }
     }



## STEP4 STATIC FILES Using AWS S3 Bucket 
#### Step1
1. Login to aws
2. Search s3 and click
3. Create bucket-choose copy settings from existing user
4. Object ownership > choose ACLS enable
5. Disable block all public access
6. Others keep same
7. Click create bucket
8. Inside bucket create 2 folders a)static b)build

#### Step 2

1. Now select security and credentials from account eg: yournam
2. Click Users > Add Users
3. Select Aws credential type =accesskey
4. Set permissions> Copy permisssions from existing user
5. Select existing user with correct credentials
6. next > Next > create User
7. Download CSV for 
8. AccessKeyid=
9. SecretaccessKey =

#### Step 3 Update settings.py
On Local Terminal  & settings.py

`pip install boto3`

`pip install django-storages`



Inside settings.py:


     Import os
     
     
     # S3 BUCKETS CONFIG

     AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
     AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
     AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
     # AWS_S3_FILE_OVERWRITE = False

     AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
     AWS_DEFAULT_ACL = 'public-read'
     AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
     AWS_LOCATION = 'static'
     AWS_QUERYSTRING_AUTH = False
     AWS_HEADERS = {'Access-Control-Allow-Origin': '*'}

     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
     STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
     STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
     # STATIC_URL = '/static/'
     MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

     if DEBUG:
         STATICFILES_DIRS=[
         os.path.join(BASE_DIR, 'build/static'),
         ]
     else:
         STATIC_ROOT=os.path.join(BASE_DIR, 'build/static')

Note: If files are not loading or displaying there is some issue with Permissions.
Following settings have worked for trial.

               Permissions overview:

                         -Access
                         -Objects can be public

               Block public access (bucket settings):

                    - all public access
                    -Off
                    -Individual Block Public Access settings for this bucket

               Object Ownership:

                    -Object Ownership
                    -Bucket owner preferred

#In settings:

     INSTALLED APP=['storages']
     ALLOWED_HOSTS = ['*']
     DEBUG=False # to check if static files are loading.
     
#In Terminal:

          python manage.py collectstatic
          
#There might be some aws connection issues whose solutions can be found online.

IF collect static successful create super user for creating admin user fro the app.

     python manage.py createsuperuser


# Step5 INSTALL AND IMPLEMENT REST FRAMEWORK & SIMPLE JWT.

     pip install djangorestframework
     python -m pip install pillow
     pip install django-cors-headers
     pip install django-rest-passwordreset
     
#install simple jwt:

          pip install djangorestframework-simplejwt


#### Settings.py

     import os
     from pathlib import Path
     from datetime import timedelta
     import environ

     env = environ.Env()
     # reading .env file
     environ.Env.read_env()


     CORS_ORIGIN_WHITELIST=('*')
     
     #in MIDDLEWARE ADD FOLLOWING:
     'corsheaders.middleware.CorsMiddleWare',
     
     REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
     }


     SIMPLE_JWT = {
         "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
         "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
         "ROTATE_REFRESH_TOKENS": False,
         "BLACKLIST_AFTER_ROTATION": False,
         "UPDATE_LAST_LOGIN": False,

         "ALGORITHM": "HS256",
         "VERIFYING_KEY": "",
         "AUDIENCE": None,
         "ISSUER": None,
         "JSON_ENCODER": None,
         "JWK_URL": None,
         "LEEWAY": 0,

         "AUTH_HEADER_TYPES": ("Bearer",),
         "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
         "USER_ID_FIELD": "id",
         "USER_ID_CLAIM": "user_id",
         "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

         "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
         "TOKEN_TYPE_CLAIM": "token_type",
         "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

         "JTI_CLAIM": "jti",

         "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
         "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
         "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

         "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.MyTokenObtainPairSerializer",
         "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
         "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
         "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
         "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
         "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
     }




INSTALLED_APPS = [
                   
    ...
    'corsheaders',
    'storages',
    'rest_framework',
    'django_rest_passwordreset',
    'rest_framework_simplejwt',
    'myapp.apps.MyappConfig',

]

### 5.1 Set up Models in Myapp
Remember not in project
Open default models.py

code: 

    from django.db import models

    from django.contrib.auth.models import User

    class Myapp(models.Model):

         name=models.CharField(max_length=130)
         image=models.ImageField(upload_to="events")
         status=models.BooleanField(default=True)
         user=models.ForeignKey(User, db_column="user", on_delete=models.CASCADE)

         def __str__(self):
             return str(self.name)

 

##### 5.1a Add Model to admin
In the myapp folder there will be a default admin.py file. open that then do as following.

          from django.contrib import admin
          from .models import *
          # Register your models here.
          class MyappAdmin(admin.ModelAdmin):
              list_display =( 'name','user')
              list_filter = ('user',)
          admin.site.register(Myapp,MyappAdmin)




In Terminal 

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py createsuperuser` # to create admin user


### 5.3 Setup Serializers in the same folder inside myapp
create new file serialisers.py

          from rest_framework import serializers;
          from .models import (Myapp, and other models)
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
          class MyappSerializer(serializers.ModelSerializer):
              class Meta:
                  model=Myapp
                  fields="__all__"


### SETTING UP VIEWS 
inside views.py

          from .models import *
          from .serializers import (MyappSerializer,
          
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

         
          class ProfileListView(APIView):
              permission_classes =([IsAuthenticated,])
              def get(self, request,format=None):
                  query=request.user
                  serializer=UserSerializer(query, many=False)
                  return Response(serializer.data)
                  # return Response("Is Authenticated by token")
                  
                  
          # Create your views here.

          class MyappListView(APIView):
              permission_classes = (IsAuthenticated,)
              def get(self, request,format=None):
                  query=Myapp.objects.filter(user=request.user)
                  serializer=MyappSerializer(query, many=True)
                  return Response(serializer.data)

              def post(self,request,format=None):
                   serializer=MyappSerializer(data=request.data)
                   if serializer.is_valid():
                          serializer.save()
                          return Response(serializer.data, status=status.HTTP_201_CREATED)
                   return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

          class MyappDetailView(APIView):
              permission_classes = (IsAuthenticated,)
              def get_object(self, pk):
                  try:
                      return Myapp.objects.get(pk=pk)
                  except Myapp.DoesNotExist:
                      raise Http404

              def get(self, request, pk, format=None):
                      query=self.get_object(pk)
                      serializer=MyappSerializer(query)
                      return Response(serializer.data)

              def put(self, request, pk, format=None):
                      query=self.get_object(pk)
                      serializer=MyappSerializer(query, request.data)
                      if serializer.is_valid():
                           serializer.save
                           return Response(serializer.data)
                      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


              def delete(self, request, pk, format=None):
                      query=self.get_object(pk)
                      model.delete()
                      return Response(status=status.HTTP_204_NO_CONTENT)







### 6.5 Set up Urls

1. creat a new folder urls, then create 2 files as below:
2. urls_myapp.py

               from django.conf import settings
               from django.conf.urls.static import static
               from django.urls import path,include
               from ..views import *

               urlpatterns=[
                   path('/', MyappListView.as_view(), name='category'),
                   path('/<int:pk>', MyappDetailView.as_view(), name='category_detail'),
               ]



4. urls_user.py

               from django.conf import settings
               from django.conf.urls.static import static
               from django.urls import path,include
               from ..views import ProfileListView, MyTokenObtainPairView,UserRegistrationView,ChangePasswordView

               urlpatterns=[
                 path('register/', UserRegistrationView.as_view(), name='user_registration'),
                 path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                 path('change-password/', ChangePasswordView.as_view(), name='change-password'),
                 path('reset-password/', include('django_rest_passwordreset.urls', namespace='reset_password')),
                 path('profile/', ProfileListView.as_view(), name='userprofile'),
                 ]



#### Update Project URLS.py file

          """api URL Configuration

          The `urlpatterns` list routes URLs to views. For more information please see:
              https://docs.djangoproject.com/en/4.1/topics/http/urls/
          Examples:
          Function views
              1. Add an import:  from my_app import views
              2. Add a URL to urlpatterns:  path('', views.home, name='home')
          Class-based views
              1. Add an import:  from other_app.views import Home
              2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
          Including another URLconf
              1. Import the include() function: from django.urls import include, path
              2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
          """
          from django.contrib import admin
          from django.urls import path, include

          urlpatterns = [
              path('api/', include("myapp.urls.urls_myapp")),
              path('api/user/', include("myapp.urls.urls_user")),
              path('admin/', admin.site.urls),
          ]


# 7.Django Signals

Add following in Models to send rest password email



          """
          To send email in forget password
          """

          from django.dispatch import receiver
          from django.urls import reverse
          from django_rest_passwordreset.signals import reset_password_token_created
          from django.core.mail import send_mail  


          @receiver(reset_password_token_created)
          def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

              email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

              send_mail(
                  # title:
                  "Password Reset for {title}".format(title="Purchase App"),
                  # message:
                  "Some one requested for password reset, please click link to reset password. " "http://127.0.0.1:8000%s"%email_plaintext_message,
                  # from:
                  "noreply@blackwood.com.hk",
                  # to:
                  [reset_password_token.user.email]
              )
  
  Create signals.py file in project folder and add following.
  
          from django.db.models.signals import pre_save
          from django.contrib.auth.models import User

          def updateUser(sender, instance, **kwargs):
              user=instance
              if user.email!="":
                  user.username=user.email

          pre_save.connect(updateUser, sender=User)
          
 
Then in Myapp folder Apps.py add following

       
              name = 'myapp'
              #Just below name add following. because sigal file is coming from api project folder

              def ready(self):
                  import api.signals
                  
## SEND EMAIL FROM DJANGO APP:
EMAIL SET UP

          EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
          EMAIL_HOST = env("EMAIL_HOST"),
          EMAIL_HOST_USER = env("EMAIL_HOST_USER"),
          EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD"),
          EMAIL_PORT = 587
          EMAIL_USE_TLS = False
          DEFAULT_FROM_EMAIL = 'My Website <noreply@mysite.com>'





#8. Before Deploying to heroku

`pip install gunicorn`


run:`gunicorn api.wsgi`
api.wsgi is the file in root folder of project.

Add Procfile to run Gunicorn server in Heroku

Indie Project folder: `touch Procfile`

Open Procfile in editor and add following:

               web: gunicorn api.wsgi
               # remember to keep space before gunicorn 
              
              
              
Add Requirements.txt 

`pip freeze>requirements.txt`


#9. Now deploying to heroku

       
Heroku
in terminal

          heroku login
          heroku create projectname

          heroku git:remote -a projectname
          heroku config:set DISABLE_COLLECTSTATIC=1
          
          git init
          git add .
          git commit -m'First-commit'

          # to remove git init
          rm rf .git


Then Push to heroku

          git push heroku master
          
          Note: IF any trouble easy to find solutions online regarding heroku.
 
Setting up all variables of Local .env file in hereku:

          Go to Settings> Config Vars >Then Key =Value 
          Save


