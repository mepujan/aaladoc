# Generated by Django 3.2.5 on 2022-02-20 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0002_auto_20220220_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicinfo',
            name='reg_year',
            field=models.DateField(null=True),
        ),
    ]
