# Generated by Django 5.0.3 on 2024-06-22 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Data_Collection', '0010_alter_buff163_options_alter_skinout_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='personalMarketData',
        ),
        migrations.DeleteModel(
            name='buff163',
        ),
        migrations.DeleteModel(
            name='skinout',
        ),
        migrations.DeleteModel(
            name='skinport',
        ),
        migrations.DeleteModel(
            name='steam',
        ),
    ]