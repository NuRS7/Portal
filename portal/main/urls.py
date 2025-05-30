from django.urls import path
from . import views
from .views import zhukteme_list, zhukteme_export

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('zhukteme_create/', views.zhukteme_create, name='zhukteme_create'),
    path('zhukteme/export/', zhukteme_export, name='zhukteme_export'),
    path('change_password/', views.change_password, name='change_password'),
#ADMIN
    path('register_teacher/', views.register_teacher, name='register_teacher'),
    path('register_student/', views.register_student, name='register_student'),
    path('kurator_top/', views.kurator_top, name='kurator_top'),
    path('sabak_top/', views.sabak_top, name='sabak_top'),
#TEACHER
    path('lek_pr/', views.lek_pr, name='lek_pr'),
    path('select_lek/<int:group_id>+<int:sabak_id>/', views.select_lek, name='select_lek'),
    path('list_lek/<int:group_id>/<int:sabak_id>/', views.list_lek, name='list_lek'),
    path('teacher_sabak/<int:sabak_turu_id>', views.teacher_sabak, name='teacher_sabak'),
    path('kurator/<int:group_id>', views.kurator, name='kurator'),
    path('tobym/', views.tobym, name='tobym'),
    path('select_group_sabak/<int:group_id>+<int:sabak_id>/', views.select_group_sabak, name='select_group_sabak'),
    path('grade_group_students/<int:group_id>/<int:sabak_id>/<int:week>/', views.grade_group_students,
         name='grade_group_students'),
#CTUDENT
    path('student_sabak/', views.student_sabak, name='student_sabak'),
    path('profile/course/<int:course_id>/', views.course_grades, name='course_grades'),

#
    path('grade_list/', views.grade_list, name='grade_list'),
    path('zhukteme/', zhukteme_list, name='zhukteme_list')
]

