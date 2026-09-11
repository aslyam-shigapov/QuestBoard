from django.urls import path
from . import views

# Пространство имён приложения
app_name = 'boards'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('list/', views.board_list, name='board_list'),
]