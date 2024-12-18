from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def profile_view(request):
    kurator = Toby_kurator.objects.filter(kurator = request.user)
    return render(request, 'main/profile.html', {'user': request.user,'kurator' : kurator})


def user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    kurator = Toby_kurator.objects.filter(kurator=request.user, group = user.toby)
    return render(request, 'main/user.html', {'users': user,'kurator' : kurator})

@login_required
def profile_update(request):
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to a success page or the profile page
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'main/profile_update.html', {'form': form,'kurator' : kurator})

@login_required
def change_password(request):
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/change_password.html', {'form': form,'kurator' : kurator})


#ADMIN

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = TeacherCreationForm()
    return render(request, 'main/admin/register_teacher.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StudentCreationForm()
    return render(request, 'main/admin/register_student.html', {'form': form})


def kurator_top(request):
    top = Toby.objects.all()
    teacher = CustomUser.objects.filter(is_teacher=True)
    if request.method == 'POST':
        form = KuratorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = KuratorForm()
    return render(request, 'main/admin/toby_kurator.html', {'form': form,'top': top ,'teacher': teacher})

def sabak_top (request):
    sabak_turu = Sabak_turu.objects.all()
    top = Toby.objects.all()
    sabak = Sabak.objects.all()
    teacher = CustomUser.objects.filter(is_teacher=True)
    if request.method == 'POST':
        form = SabakForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = SabakForm()
    return render(request, 'main/admin/sabak_top.html', {'form': form,'sabak_turu': sabak_turu,'sabak': sabak,'top': top ,'teacher': teacher})


#TEACHER

def lek_pr(request):
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    sabak_turu = Sabak_turu.objects.all()
    return render(request, 'main/teacher/lek_pr.html', {'user': request.user,'sabak_turu' : sabak_turu,'kurator' : kurator})


def kurator(request,group_id):
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    tobym = Toby_kurator.objects.filter(kurator=request.user, group = group_id)
    students = CustomUser.objects.filter(toby=group_id)
    return render(request, 'main/teacher/kurator.html', {'user': request.user,'tobym' : tobym,'students' : students,'kurator' : kurator})


def tobym(request):
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    tobym = Toby_kurator.objects.filter(kurator=request.user)
    return render(request, 'main/teacher/tobym.html', {'user': request.user,'tobym':tobym,'kurator' : kurator})


@login_required
def teacher_sabak(request,sabak_turu_id):
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    teacher_sabak = Sabak_teacher_toby.objects.filter(teacher=request.user)
    tody = Sabak_teacher_toby.objects.filter(teacher=request.user,sabak_turu = sabak_turu_id)

    return render(request, 'main/teacher/teacher_sabak.html', {'tody': tody,'kurator' : kurator})


def select_lek(request, group_id, sabak_id):
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    group = get_object_or_404(Toby, id=group_id)
    sabak = get_object_or_404(Sabak, id=sabak_id)
    leks = Sabak_lek.objects.filter( sabak=sabak, group=group)
    week = Week.objects.all()
    if request.method == 'POST':
        form = SelectLekForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(teacher=request.user)
            return redirect('teacher_sabak', sabak_turu_id = 1)
    else:
        form = SelectLekForm()

    return render(request, 'main/teacher/select_lek.html', {
        'form': form,
        'groups': [group],
        'sabaks': [sabak],
        'kurator': kurator,
        'week': week,
        'leks': leks
    })

def list_lek(request, group_id, sabak_id):
    teacher = request.user
    group = get_object_or_404(Toby, id=group_id)
    sabak = get_object_or_404(Sabak, id=sabak_id)
    leks = Sabak_lek.objects.filter( sabak=sabak, group=group)
    return render(request, 'main/teacher/list_lek.html', {'leks': leks})


def select_group_sabak(request, group_id, sabak_id,):
    week = Week.objects.all()
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    groups = Toby.objects.filter(id = group_id)
    sabaks =  Sabak.objects.filter(id = sabak_id)
    if request.method == 'POST':
        form = SelectGroupSabakForm(request.POST)
        if form.is_valid():
            group_id = form.cleaned_data['group'].id
            sabak_id = form.cleaned_data['sabak'].id
            week_id = form.cleaned_data['week'].id
            return redirect('grade_group_students', group_id=group_id, sabak_id=sabak_id, week=week_id)
    else:
        form = SelectGroupSabakForm()
    return render(request, 'main/teacher/select_list_student.html', {'form': form, 'week': week, 'groups': groups, 'sabaks': sabaks,'kurator' : kurator })

def grade_group_students(request, group_id, sabak_id, week):
    kurator = Toby_kurator.objects.filter(kurator=request.user)
    teacher = request.user
    grades = Grade.objects.filter(teacher=teacher, sabak=sabak_id, week = week, group = group_id)
    group = get_object_or_404(Toby, id=group_id)
    sabak = get_object_or_404(Sabak, id=sabak_id)
    students = CustomUser.objects.filter(toby=group_id)
    week_instance = get_object_or_404(Week, id=week)
    if request.method == 'POST':
        form = GroupGradeForm(request.POST, group=group, sabak=sabak)
        if form.is_valid():
            for student in students:
                grade_value = form.cleaned_data.get(f'grade_{student.id}')
                grade, created = Grade.objects.update_or_create(
                    student=student,
                    group=group,
                    teacher=request.user,
                    week=week_instance,
                    sabak=sabak,
                    defaults={'grade': grade_value}
                )
            return redirect('select_group_sabak', group_id = group_id,sabak_id = sabak_id)
    else:
        form = GroupGradeForm(group=group, sabak=sabak)

    return render(request, 'main/teacher/list_student.html', {'grades': grades,'form': form, 'group': group, 'sabak': sabak,'week': week,'kurator' : kurator})



#STUDENT

@login_required
def student_sabak(request):
    student = request.user
    if student.is_student and student.toby:
        courses = Sabak_teacher_toby.objects.filter(toby=student.toby)
    else:
        courses = None
    return render(request, 'main/student/student_sabak.html', {'courses': courses})


def course_grades(request, course_id):
    student = request.user
    course = get_object_or_404(Sabak, id=course_id)
    grades = Grade.objects.filter(student=student, sabak=course)

    return render(request, 'main/student/course_grades.html', {'grades': grades, 'course': course})









def grade_list(request):
    grades = Grade.objects.all().order_by('group', 'student')
    return render(request, 'main/grade.html', {'grades': grades})

