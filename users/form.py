
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Class, StudentClassAssignment, Subject, Timetable, UserProfile , TeacherClassAssignment


class CustomRegistraionForm(UserCreationForm):
    
    email = forms.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message="Phone number must be entered in the format: '+999999999'.")
    phone = forms.CharField(validators=[phone_regex], max_length=17)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        

class UserCreationFormWithRole(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        
            role = self.cleaned_data['role']
            user_profile = UserProfile(user=user, role=role)
            user_profile.save()

        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
        
        
class AddClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['classes', 'grade']

    
class AddSubForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subname', 'code']
        
        
class TeacherClassAssignmentForm(forms.ModelForm):
    
    class Meta:
        model = TeacherClassAssignment
        fields = ['user','classes', 'grade' , 'sub_name']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     classes = cleaned_data.get('classes')
    #     grade = cleaned_data.get('grade')
    #     sub_name = cleaned_data.get('sub_name')
    #     user = cleaned_data.get('user')

    #     if user and classes and grade and sub_name:
        
    #         existing_assignment = TeacherClassAssignment.objects.filter(
    #             classes=classes,
    #             grade=grade,
    #             sub_name=sub_name
    #         ).exclude(user=user).exists()  
    #         if existing_assignment:
    #             raise forms.ValidationError(
    #                 "This class, grade, and subject combination is already assigned to another teacher."
    #             )

    #     return cleaned_data

class StudentClassAssignmentForm(forms.ModelForm):
    
    class Meta:
        model = StudentClassAssignment
        fields = ['user', 'classes', 'grade']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     classes = cleaned_data('classes')
    #     grade = cleaned_data('grade')
    #     user = cleaned_data.get('user')
        
    #     if user:
        
    #         existing_assignment = StudentClassAssignment.objects.filter(
    #             classes=classes,
    #             grade=grade,
    #         ).exclude(user=user).exists()  
    #         if existing_assignment:
    #             raise forms.ValidationError(
    #                 "already assigned to student."
    #             )


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['teacher_assignment', 'day_of_week', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

