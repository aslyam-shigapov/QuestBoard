from django.urls import path
from .api import MyProfileAPIView

app_name = 'users_api'

urlpatterns = [
    path('me/', MyProfileAPIView.as_view(), name='me'),
]