from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

  
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    attendance_count = models.IntegerField(default=0) 
    last_login_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} (role: {self.role})"

    def increment_attendance(self):
        """Increment the attendance count for the user if it's a new day."""
        today = timezone.now().date() 
        if self.last_login_date != today:  
            self.attendance_count += 1
            self.last_login_date = today  
            self.save()

class Class(models.Model):
    
    classes =  models.IntegerField(null=True)
    grade =  models.CharField(max_length=50, null=True, default=None)
    
    def __str__(self):
        return f"{self.classes} - {self.grade}"

                                         
class Subject(models.Model):
    
    subname = models.CharField(max_length=100)
    code = models.CharField(max_length=10, default= 00)
    
    def __str__(self):
        return f"{self.subname} - {self.code}"
    

class StudentClassAssignment(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="student_assignments", null=True)
    grade = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="grade_assignments", null=True, default=None)
    
    def __str__(self):
        return f"{self.user.username} - {self.classes.classes} ({self.grade.grade})"


class TeacherClassAssignment(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE,related_name="teacher_assignments", null=True)
    grade = models.ForeignKey(Class, on_delete=models.CASCADE,related_name="teacher_grade_assignments", null=True, default= None)
    sub_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
   
    def __str__(self):
        return f"{self.user.username} - {self.classes.classes} ({self.grade.grade}) - {self.sub_name.subname}"


class Timetable(models.Model):
    
    teacher_assignment = models.ForeignKey(TeacherClassAssignment, on_delete=models.CASCADE)  
    day_of_week = models.CharField(max_length=10) 
    start_time = models.TimeField() 
    end_time = models.TimeField() 

    def __str__(self):
        return f"{self.teacher_assignment.user.username} - ({self.teacher_assignment.classes}) - {self.teacher_assignment.sub_name.subname} - {self.day_of_week} ({self.start_time} - {self.end_time})"      