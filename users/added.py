
# #views.py
# @login_required
# def generate_stu_marks(request):
    
#     user = request.user
 
#     exams = Exam.objects.filter(teacher_assignment__user=request.user)
#     teacher_assignment = TeacherClassAssignment.objects.filter(user=user).first()

#     marks = ExamMarks.objects.filter(
#             exam__teacher_assignment=teacher_assignment
#         ).select_related(
#             'student_assignment', 'exam', 'exam__teacher_assignment'
#         )
#     completed_exams = exams.filter(is_completed=True)

#     if request.method == 'POST':
#         form = MarksForm(request.POST, user=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Marks have been successfully generated.')
#             return redirect('generate-stu-marks')  
#     else:
#         form = MarksForm(user=request.user)

#     return render(request, 'marks/add_marks.html', {
#         'form': form,
#         'marks': marks,
#         'completed_exams': completed_exams,
#     })
    
# #form.py
# class MarksForm(forms.ModelForm):
    
#     class Meta:
#         model = ExamMarks
#         fields = ['student_assignment', 'exam', 'generated_marks']
        
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  
#         super().__init__(*args, **kwargs)
        
#         if user:
#             teacher_assignment = TeacherClassAssignment.objects.filter(user=user).first()
            
#             if teacher_assignment:
#                 self.fields['student_assignment'].queryset = StudentClassAssignment.objects.filter(
#                     classes=teacher_assignment.classes,
#                     grade=teacher_assignment.grade
#                 )
                
#                 self.fields['exam'].queryset = Exam.objects.filter(
#                     teacher_assignment__user=user,
#                     teacher_assignment__classes=teacher_assignment.classes,
#                     teacher_assignment__grade=teacher_assignment.grade,
#                     is_completed=True
#                 )
#             else:
#                 self.fields['student_assignment'].queryset = StudentClassAssignment.objects.none()
#                 self.fields['exam'].queryset = Exam.objects.none()
#         else:
#             self.fields['student_assignment'].queryset = StudentClassAssignment.objects.none()
#             self.fields['exam'].queryset = Exam.objects.none()
            
#     def clean_generated_marks(self):
#         generated_marks = self.cleaned_data['generated_marks']
#         exam = self.cleaned_data.get('exam')
#         student_assignment = self.cleaned_data.get('student_assignment')
        
#         if exam and student_assignment:
          
#             existing_marks = ExamMarks.objects.filter(
#                 student_assignment=student_assignment,
#                 exam=exam
#             ).exists()
            
#             if existing_marks:
#                 raise forms.ValidationError(f"Marks for this student in the selected exam have already been generated.")
            
#             if generated_marks > exam.marks:
#                 raise forms.ValidationError(f"Marks cannot be greater than the maximum exam marks of {exam.marks}.")
        
#         return generated_marks

# #models.py
# class StudentClassAssignment(models.Model):
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     classes = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="student_assignments", null=True)
#     grade = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="grade_assignments", null=True, default=None)
    
#     def __str__(self):
#         return f"{self.user.username} - {self.classes.classes} ({self.grade.grade})"


# class TeacherClassAssignment(models.Model):
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     classes = models.ForeignKey(Class, on_delete=models.CASCADE,related_name="teacher_assignments", null=True)
#     grade = models.ForeignKey(Class, on_delete=models.CASCADE,related_name="teacher_grade_assignments", null=True, default= None)
#     sub_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
   

#     def __str__(self):
#         return f"{self.user.username} - {self.classes.classes} ({self.grade.grade}) - {self.sub_name.subname}"
    
# class ExamMarks(models.Model):
    
#     student_assignment = models.ForeignKey(StudentClassAssignment, on_delete=models.CASCADE)
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     generated_marks = models.DecimalField(max_digits=5, decimal_places=2) 

#     def __str__(self):
#         return f"stu: {self.student_assignment.user.username}({self.student_assignment.classes}) - sub: {self.exam.teacher_assignment.sub_name.subname} - marks: {self.generated_marks}"

# class Exam(models.Model):
    
#     teacher_assignment = models.ForeignKey(TeacherClassAssignment, on_delete=models.CASCADE)  
#     exam_date = models.DateField()  
#     exam_time = models.TimeField()
#     marks = models.IntegerField(default=0) 
#     is_completed = models.BooleanField(default=False)   

#     def __str__(self):
        
#         return f"Exam: ({self.teacher_assignment.classes}) {self.teacher_assignment.sub_name.subname} ({self.exam_date}) marks: {self.marks}"
 
#  #studentdashboardpage
# {% extends "school/base.html" %}

# {% block content %}

# <div class="container-lg">
#    <h1>Student Dashboard</h1>
#    <hr>
#    <p> Hello , {{user.username}}<br><br>
#    <a class="btn btn-primary" href="{% url 'student-profile' %}" role="button">Profile</a>
#    <a class="btn btn-primary" href="{% url 'stu-view-exams' %}" role="button">Exam Schedules</a>
#    <a class="btn btn-primary" href="{% url 'stu-view-marks' %}" role="button">Exam Marks</a>
  
# </div>
# {% endblock %}

# i want that particular student view their exam marks..only particular class and exam belongs to the student and teacher added Marks
# of that student then student view their exam marks 
