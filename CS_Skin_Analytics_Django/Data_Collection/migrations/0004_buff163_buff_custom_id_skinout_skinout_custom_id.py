# Generated by Django 5.0.3 on 2024-06-21 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data_Collection', '0003_alter_buff163_table_alter_skinout_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buff163',
            name='buff_custom_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='skinout',
            name='skinout_custom_id',
            field=models.IntegerField(null=True),
        ),
    ]
