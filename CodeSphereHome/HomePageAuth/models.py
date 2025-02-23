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

#  Custom User Manager


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
        """Creates and returns a superuser using the custom User model"""
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

#  Custom User Model (For App Users: Students, Teachers)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set", blank=True)

    def __str__(self):
        return self.username

#  Profile Model (For additional user details)


class Profile(models.Model):
    #  Faculty Types
    FACULTY_CHOICES = [
        ('technology', 'Faculty of Technology'),
        ('medical', 'Faculty of Medical Science'),
        ('MBA', 'Faculty of Management Studies'),
        ('arts', 'Faculty of Arts'),
    ]

    #  Degree Types
    DEGREE_CHOICES = [
        ('btech', 'B.Tech'),
        ('mtech', 'M.Tech'),
        ('mbbs', 'MBBS'),
        ('msc', 'M.Sc'),
        ('bsc', 'B.Sc'),
        ('ba', 'B.A'),
        ('ma', 'M.A'),
    ]

    #  Branches (Engineering Example)
    BRANCH_CHOICES = [
        ('ce', 'Computer Engineering'),
        ('ec', 'Electronics & Communication'),
        ('ch', 'Chemical Engineering'),
        ('me', 'Mechanical Engineering'),
        ('mh', 'Mechatronics Engineering'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)

    faculty_type = models.CharField(
        max_length=50, choices=FACULTY_CHOICES, blank=True, null=True)
    degree_type = models.CharField(
        max_length=50, choices=DEGREE_CHOICES, blank=True, null=True)
    branch = models.CharField(
        max_length=50, choices=BRANCH_CHOICES, blank=True, null=True)
    semester = models.PositiveIntegerField(
        blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to="profile_pics/", default="default.jpg", blank=True, null=True)

    contact_number = models.CharField(max_length=15, blank=True, null=True)
    father_contact_number = models.CharField(
        max_length=15, blank=True, null=True)
    mother_contact_number = models.CharField(
        max_length=15, blank=True, null=True)

    social_links = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.user.username
