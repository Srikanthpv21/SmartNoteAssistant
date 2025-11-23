# mysite/assistant/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('summarize/', views.summarize_text, name='summarize_text'),
    path('history/', views.history_list, name='history_list'),
    path('summary/<int:pk>/', views.summary_detail, name='summary_detail'),
    path('download/<int:summary_id>/', views.download_summary, name='download_summary'),
]