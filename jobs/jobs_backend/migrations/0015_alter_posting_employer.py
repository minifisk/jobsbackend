# Generated by Django 3.2.4 on 2021-06-30 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_backend', '0014_auto_20210629_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='employer',
            field=models.ForeignKey(limit_choices_to={'is_employer': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='related employer'),
        ),
    ]
