
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .form import AddClassForm, AddSubForm, CustomRegistraionForm, StudentClassAssignmentForm,TeacherClassAssignmentForm, TimetableForm ,UserCreationFormWithRole 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import Class, StudentClassAssignment, Subject, TeacherClassAssignment, Timetable, UserProfile 
from django.contrib.auth.models import User
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount

# Create your views here.

def is_admin(user):
    return user.is_superuser

def not_authorized(request):
    return render (request, 'users/not_auth.html')


@user_passes_test(is_admin, login_url='not_authorized')
def register(request):
    
    if request.method == 'POST':
        
        form = CustomRegistraionForm(request.POST)
        
        if form.is_valid():
            
            user = form.save()  
            UserProfile.objects.create(user=user, role='student') 
            auth_login(request, user)
            messages.success(request, "Your account has been created successfully! You can login now.")

            return redirect('login')      
    else:
        form = CustomRegistraionForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  
        
            try:
                social_account = SocialAccount.objects.get(user=user)
                is_social_login = True  
            except SocialAccount.DoesNotExist:
                is_social_login = False 

            try:
                user_profile = UserProfile.objects.get(user=user)
                role = user_profile.role
                
                today = timezone.now().date()  
                if user_profile.last_login_date != today: 
                    user_profile.increment_attendance()  
                    
            except UserProfile.DoesNotExist:              
                
                if is_social_login:         
                    role = 'student'  

            if role == 'admin':
                return redirect('admin-dash')  
            elif role == 'teacher':
                return redirect('teacher-dash')  
            elif role == 'student':
                return redirect('student-dash')  
            else:
                messages.error(request, "Your role is not defined.")
                return redirect('login')  

        else:
            messages.error(request, "Invalid username or password.") 

    return render(request, 'users/login.html')


@login_required
@user_passes_test(is_admin)
def admin_dash(request): 
    return render(request, 'users/admindashboard.html')

@login_required
def user_dash(request): 
    return render(request, 'users/userdashboard.html')

@login_required
def teacher_dash(request): 
    return render(request, 'users/teacherdashboard.html')

@login_required
def student_dash(request): 
    return render(request, 'users/studentdashboard.html')


@login_required
@user_passes_test(is_admin)
def admin_profile(request):
    user = request.user
    try:
   
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        
        user_profile = UserProfile.objects.create(user=user, role='admin')  

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()  

        return redirect('admin-profile')  
    
    return render(request, 'users/adminprofile.html', {'user_profile': user_profile})


@login_required
def teacher_profile(request):
    user = request.user
    
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user, role='teacher')  
    
    teacher_assignment = TeacherClassAssignment.objects.filter(user=user).first() 

    if teacher_assignment:
        teacher_class = teacher_assignment.classes 
        teacher_subject = teacher_assignment.sub_name.subname  
    else:
        teacher_class = None
        teacher_subject = None 

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()  

        return redirect('teacher-profile')  

    return render(request, 'users/teacherprofile.html', {
        'user_profile': user_profile,
        'teacher_class': teacher_class,
        'teacher_subject': teacher_subject
    })
    

@login_required
def student_profile(request):
    user = request.user
    
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user, role='student')
    
    student_assignment = StudentClassAssignment.objects.filter(user=user).first() 

    if student_assignment:
        student_class = student_assignment.classes 
        student_grade = student_assignment.grade  
    else:
        student_class = None
        student_grade = None

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()  

        return redirect('student-profile')  
    
    return render(request, 'users/studentprofile.html', {
        'user_profile': user_profile,
        'student_class': student_class,
        'student_grade': student_grade
    })


@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        form = UserCreationFormWithRole(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('admin-dash')  
    else:
        form = UserCreationFormWithRole()
    
    return render(request, 'users/add_user.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def add_class(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        form = AddClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class created successfully!")
            return redirect('add-class')  
    else:
        form = AddClassForm()
    
    return render(request, 'users/add_class.html', {'form': form, 'classes': classes})


@login_required
@user_passes_test(is_admin)
def add_subject(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        form = AddSubForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "subject created successfully!")
            return redirect('add-sub')  
    else:
        form = AddSubForm()
    
    return render(request, 'users/add_sub.html', {'form': form , 'subjects':subjects})


@login_required
@user_passes_test(is_admin)
def assign_teacher(request):
    
    teachers = TeacherClassAssignment.objects.all()
    if request.method == 'POST':
        form = TeacherClassAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Assigned sub-class to teacher successfully!")
            return redirect('assign-teacher')
    else:
        teacher_users = UserProfile.objects.filter(role='teacher')
        form = TeacherClassAssignmentForm()

        form.fields['user'].queryset = teacher_users

    return render(request, 'users/assign_teacher.html', {'form': form, 'teachers': teachers})


@login_required
@user_passes_test(is_admin)
def assign_student(request):
    
    students = StudentClassAssignment.objects.all()
    if request.method == 'POST':
        form = StudentClassAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Assigned class to student successfully!")
            return redirect('assign-student')  
    else:
        student_users = UserProfile.objects.filter(role='student')
        form = StudentClassAssignmentForm()
        
        form.fields['user'].queryset = student_users
    
    return render(request, 'users/assign_student.html', {'form': form, 'students': students})


@login_required
@user_passes_test(is_admin)
def add_timetable(request):
    
    timetables = Timetable.objects.all()

    if request.user.is_superuser:
        # timetables = Timetable.objects.all() 
        if request.method == 'POST':
            form = TimetableForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Timetable has been successfully added.")
                return redirect('add-timetable')  
        else:
            form = TimetableForm()

    return render(request, 'users/add_timetable.html', {'form': form, 'timetables':timetables})
   

@login_required
@user_passes_test(is_admin)
def display_users(request):
    
    search_query = request.GET.get('search', '')  

    if search_query:
        users = User.objects.filter(
            username__icontains=search_query
        ) | User.objects.filter(
            email__icontains=search_query
        )
    else:
        users = User.objects.all()

    return render(request, 'users/displayusers.html', {'users': users})


@login_required
def display_students(request):
    students = StudentClassAssignment.objects.all()
    return render(request, 'users/displaystudents.html',{'students': students})

@login_required
def view_timetable(request):
    timetables = Timetable.objects.all()
    return render(request, 'users/display_timetable.html', {'timetables': timetables})


@login_required
def update_timetable(request, timetable_id):

    timetable = get_object_or_404(Timetable, id=timetable_id)  

    if request.method == 'POST':

        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('add-timetable')  
    else:
      
        form = TimetableForm(instance=timetable)

    return render(request, 'users/update_timetable.html', {'form': form})

@login_required
def delete_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)
    
    timetable.delete()
    return redirect('add-timetable') 

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('display-users')


@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":

        # user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('display-users')

    return render(request, 'users/update_user.html', {'user': user})


@login_required
def logout(request):
    return redirect('login')

# @login_required
# def display_timetables(request):
#     if request.user.is_superuser:  # Ensure only admin can view
#         timetables = Timetable.objects.all()  # Get all timetables
#         return render(request, 'admin/display_timetables.html', {'timetables': timetables})

#     else:
#         messages.error(request, "You do not have permission to access this page.")
#         return redirect('admin-dashboard')

