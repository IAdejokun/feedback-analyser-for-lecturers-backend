# Generated by Django 5.0.6 on 2024-08-02 01:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.universities'),
        ),
    ]
