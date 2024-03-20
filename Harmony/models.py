from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, username=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, username=None):
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(unique=True, max_length=20)
    username = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class SignIn(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)

    def _str_(self):
        return self.email


# def signup(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         phone_number = request.POST['phone_number']
#         password = request.POST['password']
#         username = request.POST.get('username', None)

#         user = CustomUser.objects.create_user(email=email, phone_number=phone_number, password=password,
#                                               username=username)
#         # Custom logic or redirects after successful sign-up
#         return render(request, 'signup_success.html', {'user': user})

#     return render(request, 'signup.html')


# class CustomLoginView(LoginView):
#     template_name = 'login.html'
#     # Additional customizations for login view


# def home(request):
#     # Your home view logic here
#     return render(request, 'home.html')