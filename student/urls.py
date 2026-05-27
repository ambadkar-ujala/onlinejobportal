from django.urls import path
from . import views

urlpatterns = [
    path('student/register/', views.register1, name='register1'),
    path('student/login/', views.login1, name='login1'),
    path('logout/', views.logout1, name='logout1'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('apply/<int:id>/', views.apply_job, name='apply'),
    path('save/<int:id>/', views.save_job, name='save'),
    path('saved_job/', views.saved_job, name='saved_job'),
    path('applied_job/', views.applied_job, name='saved_job'),
    path('change_password/', views.change_password, name='change_password'),
    path('student_details/', views.student_details, name='student_details'),
    path('update_student/<int:id>/', views.update_student, name='update_student'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('student/education/', views.student_education, name='student_education'),
    path('student/experience/', views.student_experience, name='student_experience'),
    path('edit_education/', views.edit_education, name='edit_education'),
    path('edit_education12/', views.edit_education12, name='edit_education12'),
    path('edit_educationgr/', views.edit_educationgr, name='edit_educationgr'),
    path('edit_educationpg/', views.edit_educationpg, name='edit_educationpg'),
    path('edit_exp/', views.edit_experience, name='edit_experience'),
    path('change_image/', views.change_image, name='change_image'),
    path('update_resume/', views.update_resume, name='update_resume'),
]
