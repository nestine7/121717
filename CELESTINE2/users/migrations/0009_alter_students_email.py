# Generated by Django 4.2.5 on 2023-10-30 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_students_phone_no_students_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
