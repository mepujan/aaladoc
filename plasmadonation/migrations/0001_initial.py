# Generated by Django 3.2.5 on 2021-12-18 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlasmaDonorsInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('district', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('dob', models.DateField()),
                ('blood_type', models.CharField(choices=[('O +ve', 'O +ve'), ('O -ve', 'O -ve'), ('A +ve', 'A +ve'), ('A -ve', 'A -ve'), ('B +ve', 'B +ve'), ('B -ve', 'B -ve'), ('AB +ve', 'AB +ve'), ('AB -ve', 'AB -ve')], max_length=6)),
                ('profile_picture', models.ImageField(upload_to='media')),
            ],
        ),
    ]