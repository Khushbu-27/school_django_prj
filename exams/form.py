
from django import forms
from .models import Exam, TeacherClassAssignment

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['teacher_assignment', 'exam_date', 'exam_time', 'marks', 'is_completed', 'test_paper']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['teacher_assignment'].queryset = TeacherClassAssignment.objects.filter(user=user)
        else:
            self.fields['teacher_assignment'].queryset = TeacherClassAssignment.objects.none()  
