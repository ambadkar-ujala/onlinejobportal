from django.urls import path
from . import views

urlpatterns = [
    path('ehome/', views.ehome, name='ehome'),
    path('employer/register/', views.register2, name='register2'),
    path('employer/login/', views.login2, name='login2'),
    path('employer/logout/', views.logout2, name='logout2'),
    path('post_job/', views.post_job, name='post_job'),
    path('job_list/', views.job_list, name='job_list'),
    path('candidate_applied/', views.candidate_applied, name='candidate_applied'),
    path('update_employer/', views.update_employer, name='update_employer'),
    path('edit_job/<int:id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:id>/', views.delete_job, name='delete_job'),
    path('change_emppassword/', views.change_emppassword, name='change_emppassword'),
]

