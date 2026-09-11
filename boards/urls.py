from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('list/', views.board_list, name='board_list'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('create/', views.board_create, name='board_create'),
    path('<int:board_id>/', views.board_detail, name='board_detail'),
    path('<int:board_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('<int:board_id>/edit/', views.board_edit, name='board_edit'),
    path('<int:board_id>/delete/', views.board_delete, name='board_delete'),
]