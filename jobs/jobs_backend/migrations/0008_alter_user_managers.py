# Generated by Django 3.2.4 on 2021-06-22 09:12

from django.db import migrations
import jobs_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_backend', '0007_alter_user_company_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', jobs_backend.models.CustomUserManager()),
            ],
        ),
    ]