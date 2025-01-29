
from django.db import models
from users.models import TeacherClassAssignment

# Create your models here.

class Exam(models.Model):
    
    teacher_assignment = models.ForeignKey(TeacherClassAssignment, on_delete=models.CASCADE)  
    exam_date = models.DateField()  
    exam_time = models.TimeField()
    marks = models.IntegerField(default=0) 
    is_completed = models.BooleanField(default=False)   

    def __str__(self):
        
        return f"Exam: ({self.teacher_assignment.classes}) {self.teacher_assignment.sub_name.subname} ({self.exam_date}) marks: {self.marks}"
 
