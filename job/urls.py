from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('latest_job/', views.latest_job, name='latest_job'),
    path('job_details/<int:id>/', views.job_details, name='job_details'),
]
