from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.views import CustomAuthToken
from .views import registration_view

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('register/', registration_view, name='register'),
]
