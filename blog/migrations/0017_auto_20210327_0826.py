# Generated by Django 3.0.3 on 2021-03-27 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20210324_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='alt_text',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]
