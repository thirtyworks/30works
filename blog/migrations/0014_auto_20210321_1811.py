# Generated by Django 3.0.3 on 2021-03-21 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_post_datetime_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='number',
            field=models.IntegerField(unique=True, verbose_name='Day Number'),
        ),
    ]
