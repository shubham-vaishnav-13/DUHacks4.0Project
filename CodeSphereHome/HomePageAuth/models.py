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


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role=None):
        """Creates and returns a normal user (Students, Teachers)"""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """Creates and returns a superuser using Django's default auth system"""
        from django.contrib.auth.models import User as DefaultUser  # Uses Django's auth.User
        return DefaultUser.objects.create_superuser(username, email, password)

#  Custom User Model (For App Users: Students, Teachers)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True)

    #  Override default manager
    objects = UserManager()

    #  Prevents non-admin users from accessing Django Admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)  # NEW FIELD
    groups = models.ManyToManyField(
        Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set", blank=True
    )

    def __str__(self):
        return self.username

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
        return self.user.username

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
