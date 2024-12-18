from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class StudentCreationForm(UserCreationForm):
    is_student = forms.BooleanField(required=False)
    is_teacher = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name','last_name','username', 'password1', 'password2', 'is_student', 'is_teacher',  'kyrs', 'toby', 'oku_tury',]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return password2

class TeacherCreationForm(UserCreationForm):
    is_student = forms.BooleanField(required=False)
    is_teacher = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name','last_name','username', 'password1', 'password2', 'is_student', 'is_teacher', 'dareje', 'kyzmet',]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин ", max_length=100)
    password = forms.CharField(label="Пороль ", widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'telefon', 'addres1', 'addres2',
            'ana', 'ana_nomer', 'ake', 'ake_nomer', 'about_me', 'img']

class KuratorForm(forms.ModelForm):
    class Meta:
        model = Toby_kurator
        fields = ['kurator', 'group']


class SabakForm(forms.ModelForm):
    class Meta:
        model = Sabak_teacher_toby
        fields = ['teacher','toby','sabak','sabak_turu']

class SelectGroupSabakForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Toby.objects.all(), label="Топ")
    sabak = forms.ModelChoiceField(queryset=Sabak.objects.all(), label="Сабақ")
    week  = forms.ModelChoiceField(queryset=Week.objects.all(), label="Апта")

class GroupGradeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        sabak = kwargs.pop('sabak', None)
        super(GroupGradeForm, self).__init__(*args, **kwargs)
        if group and sabak:
            students = CustomUser.objects.filter(toby = group)
            for student in students:
                self.fields[f'grade_{student.id}'] = forms.IntegerField( label=student, required=True)



class SelectLekForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Toby.objects.all(), label="Топ")
    sabak = forms.ModelChoiceField(queryset=Sabak.objects.all(), label="Сабақ")
    week  = forms.ModelChoiceField(queryset=Week.objects.all(), label="Апта")
    lek = forms.FileField(label="Лекция файлы")

    def save(self, teacher):
        data = self.cleaned_data
        sabak_lek = Sabak_lek(
            group=data['group'],
            teacher=teacher,
            sabak=data['sabak'],
            lek=data['lek'],
            week=data['week']
        )
        sabak_lek.save()
        return sabak_lek