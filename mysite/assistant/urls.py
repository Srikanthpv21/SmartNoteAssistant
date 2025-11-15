from django.urls import path
from . import views

urlpatterns = [
    # Your existing summary view
    path('', views.your_summary_view, name='summary_view'),
    
    # New path for downloading
    path('download/<int:summary_id>/', views.download_summary, name='download_summary'),
]