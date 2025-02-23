from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

#  Role Model (Defines User Roles)


class Role(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role_name = models.CharField(
        max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.role_name

#  Custom User Manager (For HomePageAuth Users)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

#  Custom User Model (For App Users: Students, Teachers)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    #  Prevents non-admin users from accessing Django Admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)  # NEW FIELD
    groups = models.ManyToManyField(
        Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set", blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.email

#  Profile Model (For additional user details)


class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # NEW FIELD
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True)  # NEW FIELD
    date_of_birth = models.DateField(blank=True, null=True)  # NEW FIELD
    social_links = models.JSONField(default=dict, blank=True)
    image = models.ImageField(
        upload_to="profile_pics/", default="default.jpg", blank=True, null=True)

    def __str__(self):
        return self.user.email

#  Login History Model (Tracks login attempts)


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    device_info = models.JSONField(default=dict)
    status = models.CharField(
        max_length=10, choices=[('Success', 'Success'), ('Failed', 'Failed')]
    )

#  Password Reset Model


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=50, unique=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
