from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_student, name='create_student'),
    path('student/<str:student_id>/', views.get_student, name='get_student'),
    path('update/<str:student_id>/', views.update_student, name='update_student'),
    path('delete/<str:student_id>/', views.delete_student, name='delete_student'),
    path('all/', views.get_all_students, name='get_all_students'),
]
