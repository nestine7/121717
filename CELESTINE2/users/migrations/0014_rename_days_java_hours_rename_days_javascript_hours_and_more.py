# Generated by Django 4.2.5 on 2023-11-05 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_jsattendance_present_phpattendance_present_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='java',
            old_name='days',
            new_name='hours',
        ),
        migrations.RenameField(
            model_name='javascript',
            old_name='days',
            new_name='hours',
        ),
        migrations.RenameField(
            model_name='php',
            old_name='days',
            new_name='hours',
        ),
        migrations.RenameField(
            model_name='python',
            old_name='days',
            new_name='hours',
        ),
        migrations.RenameField(
            model_name='sql',
            old_name='days',
            new_name='hours',
        ),
    ]
