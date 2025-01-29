
from django.urls import path 
from exams import views as exam_views

urlpatterns = [
    path('add_exam/',exam_views.add_exam, name='add-exam'),
    path('display_exams/', exam_views.dispay_exams, name='display-exams'),
    path('exams/update/<int:exam_id>/', exam_views.update_exam, name='update-exam'),
    path('exams/delete/<int:exam_id>/', exam_views.delete_exam, name='delete-exam'),
    path('stu_view_exams/', exam_views.stu_view_exams, name='stu-view-exams'),
]