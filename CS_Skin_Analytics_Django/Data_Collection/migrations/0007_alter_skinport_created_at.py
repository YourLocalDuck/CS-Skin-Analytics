# Generated by Django 5.0.3 on 2024-06-21 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data_Collection', '0006_alter_skinport_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skinport',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]