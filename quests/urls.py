from django.urls import path
from . import views

app_name = 'quests'

urlpatterns = [
    path('board/<int:board_id>/create/', views.quest_create, name='quest_create'),
    path('<int:quest_id>/delete/', views.quest_delete, name='quest_delete'),
    path('<int:quest_id>/complete/', views.quest_complete, name='quest_complete'),
]