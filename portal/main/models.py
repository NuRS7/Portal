from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class Kyrs(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)

    def __str__(self):
        return self.name


class Toby(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)

    def __str__(self):
        return self.name


class Oky_tury(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)

    def __str__(self):
        return self.name


class Dareje(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)

    def __str__(self):
        return self.name


class Kyzmet(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    img = models.ImageField('foto', upload_to="profile/", blank=True, null=True)
    data = models.DateField('tygan kyn', blank=True, null=True)
    about_me  = models.TextField('ozim jaily', blank=True, null=True)
    email = models.EmailField('email', blank=True, null=True, )
    telefon = models.CharField('telefon', blank=True, null=True, max_length=20)
    addres1 = models.CharField('meken-jai-1', blank=True, null=True, max_length=100)
    addres2 = models.CharField('meken-jai-2', blank=True, null=True, max_length=100)
    ana = models.CharField('anasy aty', blank=True, null=True, max_length=100)
    ana_nomer = models.CharField('ana_telefon', blank=True, null=True, max_length=20)
    ake = models.CharField('akesy aty', blank=True, null=True, max_length=100)
    ake_nomer = models.CharField('ake_telefon', blank=True, null=True, max_length=20)
    kyrs = models.ForeignKey(Kyrs, on_delete=models.CASCADE, verbose_name='kyrs', blank=True, null=True )
    toby = models.ForeignKey(Toby, on_delete=models.CASCADE, verbose_name='toby', blank=True, null=True)
    oku_tury = models.ForeignKey(Oky_tury, on_delete=models.CASCADE, verbose_name='oky_tury', blank=True, null=True)
    dareje = models.ForeignKey(Dareje, on_delete=models.CASCADE, verbose_name='dareje', blank=True, null=True)
    kyzmet = models.ForeignKey(Kyzmet, on_delete=models.CASCADE, verbose_name='kyzmet', blank=True, null=True)
    sabak = models.ManyToManyField(Kyrs, verbose_name='sabak', related_name='custom_user_sabaks')

    # Related names for groups and permissions
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_permissions',
        related_query_name='customuser_permission',
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='customuser_groups',
        related_query_name='customuser_group',
    )

    def __str__(self):
        return self.username

class Toby_kurator(models.Model):
    group = models.ForeignKey(Toby, on_delete=models.CASCADE)
    kurator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, )


class Sabak(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)

    def __str__(self):
        return self.name

class Sabak_turu(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)

    def __str__(self):
        return self.name

class Week(models.Model):
    name = models.CharField(verbose_name='name', max_length=100)

    def __str__(self):
        return self.name

class Sabak_teacher_toby(models.Model):
    sabak = models.ForeignKey(Sabak, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sabak_turu = models.ForeignKey(Sabak_turu, related_name='sabaks', on_delete=models.CASCADE,blank=True, null=True,)
    toby = models.ForeignKey(Toby, related_name='teachers', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.sabak)

class Sabak_lek(models.Model):
    group = models.ForeignKey(Toby, on_delete=models.CASCADE,blank=True, null=True,)
    teacher = models.ForeignKey(CustomUser, related_name='sabaks', on_delete=models.CASCADE)
    sabak = models.ForeignKey(Sabak, on_delete=models.CASCADE, blank=True, null=True, )
    lek = models.FileField(upload_to='documents/')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, blank=True, null=True, )
    date = models.DateField(auto_now=True,blank=True, null=True,)

    def __str__(self):
        return str(self.sabak)


class Grade(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,)
    group = models.ForeignKey(Toby, on_delete=models.CASCADE,blank=True, null=True,)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_grades',blank=True, null=True,)
    sabak = models.ForeignKey(Sabak, on_delete=models.CASCADE, blank=True, null=True, )
    grade = models.IntegerField(default=0,blank=True, null=True,)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, blank=True, null=True, )
    date = models.DateField(auto_now=True,blank=True, null=True,)



