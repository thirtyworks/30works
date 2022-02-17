# Generated by Django 3.0.3 on 2021-02-25 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userprofile_date_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='contact_info',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='insta_handler',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
