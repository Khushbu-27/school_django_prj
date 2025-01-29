
from django import forms
from exams.models import Exam
from users.models import StudentClassAssignment, TeacherClassAssignment
from .models import ExamMarks


class MarksForm(forms.ModelForm):
    
    class Meta:
        model = ExamMarks
        fields = ['student_assignment', 'exam', 'generated_marks']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        
        if user:
            teacher_assignment = TeacherClassAssignment.objects.filter(user=user).first()
            
            if teacher_assignment:
                self.fields['student_assignment'].queryset = StudentClassAssignment.objects.filter(
                    classes=teacher_assignment.classes,
                    grade=teacher_assignment.grade
                )
                
                self.fields['exam'].queryset = Exam.objects.filter(
                    teacher_assignment__user=user,
                    teacher_assignment__classes=teacher_assignment.classes,
                    teacher_assignment__grade=teacher_assignment.grade,
                    is_completed=True
                )
            else:
                self.fields['student_assignment'].queryset = StudentClassAssignment.objects.none()
                self.fields['exam'].queryset = Exam.objects.none()
        else:
            self.fields['student_assignment'].queryset = StudentClassAssignment.objects.none()
            self.fields['exam'].queryset = Exam.objects.none()
            
    def clean_generated_marks(self):
        generated_marks = self.cleaned_data['generated_marks']
        exam = self.cleaned_data.get('exam')
        student_assignment = self.cleaned_data.get('student_assignment')
        
        if exam and student_assignment:
          
            existing_marks = ExamMarks.objects.filter(
                student_assignment=student_assignment,
                exam=exam
            ).exists()
            
            if existing_marks:
                raise forms.ValidationError(f"Marks for this student in the selected exam have already been generated.")
            
            if generated_marks > exam.marks:
                raise forms.ValidationError(f"Marks cannot be greater than the maximum exam marks of {exam.marks}.")
        
        return generated_marks

