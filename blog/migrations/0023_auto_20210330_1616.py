# Generated by Django 3.0.3 on 2021-03-30 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20210328_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='alt_text',
            field=models.CharField(blank=True, default=None, max_length=600, null=True),
        ),
    ]
