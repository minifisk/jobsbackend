# Generated by Django 3.2.4 on 2021-06-16 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_backend', '0002_application_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='jobs_backend.applicant', verbose_name='related applicant'),
        ),
    ]
