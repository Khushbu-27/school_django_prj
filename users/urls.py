
from django.urls import path , include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',user_views.register, name='register'),
    path('not_authorized', user_views.not_authorized, name='not_authorized'),
    path('login/', user_views.user_login, name='login'),
    path("accounts/", include("allauth.urls")),
    path('admindash/', user_views.admin_dash, name='admin-dash'),
    path('add-user/', user_views.add_user, name='add-user'),
    path('add-class/', user_views.add_class, name='add-class'),
    path('add-subject/', user_views.add_subject, name='add-sub'),
    path('add-timetable/', user_views.add_timetable, name='add-timetable'),
    path('assign-teacher/', user_views.assign_teacher, name='assign-teacher'),
    path('assign-student/', user_views.assign_student, name='assign-student'),
    path('display-users/', user_views.display_users, name='display-users'),
    path('view_timetable/', user_views.view_timetable, name='view-timetable'),
    path('update_timetable/<int:timetable_id>/', user_views.update_timetable, name='update-timetable'),
    path('delete_timetable/<int:timetable_id>/', user_views.delete_timetable, name='delete-timetable'),
    path('display_students/', user_views.display_students, name='display-students'),
    path('userdash/', user_views.user_dash, name='user-dash'),
    path('teacherdash/', user_views.teacher_dash, name='teacher-dash'),
    path('studentdash/', user_views.student_dash, name='student-dash'),
    path('teacherprofile/', user_views.teacher_profile, name = 'teacher-profile'),
    path('studentprofile/', user_views.student_profile, name = 'student-profile'),
    path('adminprofile/', user_views.admin_profile, name = 'admin-profile'),
    path('logout/', user_views.logout , name='logout'),
    path('user/delete/<int:user_id>/', user_views.delete_user, name='delete-user'),
    path('user/update/<int:user_id>/', user_views.update_user, name='update-user'),
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name = "users/reset_pass.html"), 
         name ='reset_password'
         ),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name = "users/pass_reset_sent.html"),
         name ='password_reset_done'
         ),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name = "users/pass_reset_form.html"), 
         name ='password_reset_confirm'
         ),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name = "users/pass_reset_done.html"), 
         name ='password_reset_complete'
         ),
     # path('search/', user_views.search, name="search"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)