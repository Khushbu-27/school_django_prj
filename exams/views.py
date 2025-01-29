
from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404
from .models import Exam
from.form import ExamForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import TeacherClassAssignment , StudentClassAssignment


@login_required
def add_exam(request):
    
    exams = Exam.objects.filter(teacher_assignment__user=request.user)
    teacher_assignment = TeacherClassAssignment.objects.filter(user=request.user).first()

    # if teacher_assignment is None:
    #     messages.error(request, "You are not assigned to any class")
    #     return redirect('teacher-dash')

    if request.method == 'POST':
        form = ExamForm(request.POST, user=request.user)
        if form.is_valid():
       
            exam = form.save(commit=False)
            exam.teacher_assignment = teacher_assignment  
            exam.save()
            messages.success(request, "Exam created successfully!")
            return redirect('add-exam')  
    else:
        form = ExamForm(user=request.user) 

    return render(request, 'exams/add_exam.html', {'form': form, 'exams': exams})

@login_required
def dispay_exams(request):
    exams = Exam.objects.all()
    return render(request, 'exams/displayexams.html',{'exams': exams})


@login_required
def update_exam(request, exam_id):

    exam = get_object_or_404(Exam, id=exam_id)
    
    if exam.teacher_assignment.user != request.user:
        return redirect('teacher-dash')  

    if request.method == 'POST':

        form = ExamForm(request.POST, instance=exam, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('teacher-dash')  
    else:
      
        form = ExamForm(instance=exam, user=request.user)

    return render(request, 'exams/update_exam.html', {'form': form})


@login_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if exam.teacher_assignment.user != request.user:
        return redirect('teacher-dash')  
    
    exam.delete()
    return redirect('teacher-dash')  

@login_required
def stu_view_exams(request):

    student_class_assignment = StudentClassAssignment.objects.filter(user=request.user).first()

    if student_class_assignment:
        student_class = student_class_assignment.classes
        student_grade = student_class_assignment.grade

        exams = Exam.objects.filter(
            teacher_assignment__classes=student_class,
            teacher_assignment__grade=student_grade,
        )
    else:
        exams = []

    return render(request, 'exams/stu_view_exams.html', {'exams': exams})
