from django.contrib import admin
from .models import UserProfile,TeacherClassAssignment , StudentClassAssignment , Class , Subject , Timetable

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(TeacherClassAssignment)
admin.site.register(StudentClassAssignment)
admin.site.register(Timetable)