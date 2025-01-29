
from django.urls import path 
from  marks import views as marks_view

urlpatterns = [
    
    path('generate-stu-marks/',marks_view.generate_stu_marks, name='generate-stu-marks'),
    path('stu-view-marks/',marks_view.stu_view_marks, name='stu-view-marks'),
]