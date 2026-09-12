from django.urls import path
from .api import QuestListAPIView

app_name = 'quests_api'

urlpatterns = [
    path('', QuestListAPIView.as_view(), name='list'),
]