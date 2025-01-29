from django.db import models
from exams.models import Exam
from users.models import StudentClassAssignment

# Create your models here.

class ExamMarks(models.Model):
    
    student_assignment = models.ForeignKey(StudentClassAssignment, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    generated_marks = models.DecimalField(max_digits=5, decimal_places=2) 

    def __str__(self):
        return f"stu: {self.student_assignment.user.username}({self.student_assignment.classes}) - sub: {self.exam.teacher_assignment.sub_name.subname} - marks: {self.generated_marks}"
