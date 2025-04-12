# Generated by Django 5.1.7 on 2025-04-12 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_userexpense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexpense',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='mainapp.user'),
        ),
    ]
