# Generated by Django 3.2.4 on 2021-06-23 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_backend', '0010_UPDATE_SITE_NAME'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='cv_link',
            field=models.FileField(max_length=30, upload_to=''),
        ),
    ]