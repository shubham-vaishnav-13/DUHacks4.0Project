# Generated by Django 4.2.18 on 2025-02-23 06:47

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.group')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HomePageAuth.role')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('faculty_type', models.CharField(blank=True, choices=[('technology', 'Faculty of Technology'), ('medical', 'Faculty of Medical Science'), ('MBA', 'Faculty of Management Studies'), ('arts', 'Faculty of Arts')], max_length=50, null=True)),
                ('degree_type', models.CharField(blank=True, choices=[('btech', 'B.Tech'), ('mtech', 'M.Tech'), ('mbbs', 'MBBS'), ('msc', 'M.Sc'), ('bsc', 'B.Sc'), ('ba', 'B.A'), ('ma', 'M.A')], max_length=50, null=True)),
                ('branch', models.CharField(blank=True, choices=[('ce', 'Computer Engineering'), ('ec', 'Electronics & Communication'), ('ch', 'Chemical Engineering'), ('me', 'Mechanical Engineering'), ('mh', 'Mechatronics Engineering')], max_length=50, null=True)),
                ('semester', models.PositiveIntegerField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pics/')),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('father_contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('mother_contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('social_links', models.JSONField(blank=True, default=dict)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
