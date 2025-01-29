from django.shortcuts import render , redirect
from exams.models import Exam
from .models import ExamMarks
from .form import MarksForm
from users.models import StudentClassAssignment, TeacherClassAssignment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def generate_stu_marks(request):
    
    user = request.user
 
    exams = Exam.objects.filter(teacher_assignment__user=request.user)
    teacher_assignment = TeacherClassAssignment.objects.filter(user=user).first()

    marks = ExamMarks.objects.filter(
            exam__teacher_assignment=teacher_assignment
        ).select_related(
            'student_assignment', 'exam', 'exam__teacher_assignment'
        )
    completed_exams = exams.filter(is_completed=True)

    if request.method == 'POST':
        form = MarksForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marks have been successfully generated.')
            return redirect('generate-stu-marks')  
    else:
        form = MarksForm(user=request.user)

    return render(request, 'marks/add_marks.html', {
        'form': form,
        'marks': marks,
        'completed_exams': completed_exams,
    })

@login_required
def stu_view_marks(request):
    
    user = request.user
    student_assignment = StudentClassAssignment.objects.filter(user=user).first()

    if not student_assignment:
        messages.error(request, "Student assignment not found.")
        return redirect('student-dashboard') 

    marks = ExamMarks.objects.filter(student_assignment=student_assignment).select_related('exam', 'exam__teacher_assignment')

    return render(request, 'marks/stu_view_marks.html', {'marks': marks,})
