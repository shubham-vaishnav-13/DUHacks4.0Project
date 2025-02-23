from django.db import migrations

def create_roles(apps, schema_editor):
    Role = apps.get_model('HomePageAuth', 'Role')
    Role.objects.create(role_name='student')
    Role.objects.create(role_name='teacher')

class Migration(migrations.Migration):
    dependencies = [
        ('HomePageAuth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_roles),
    ] 