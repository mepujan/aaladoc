# Generated by Django 3.2.5 on 2021-12-18 13:40

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True)),
                ('written_by', models.CharField(max_length=300)),
                ('designation', models.TextField()),
                ('institution', models.TextField()),
                ('title', ckeditor.fields.RichTextField()),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', models.CharField(default='slug', max_length=400, unique=True)),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('no_comments', models.IntegerField(blank=True, default=0)),
                ('trending', models.BooleanField(default=False)),
                ('publish', models.BooleanField(default=False)),
                ('views', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('tags', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('no_comments', models.IntegerField(default=0)),
                ('verify', models.BooleanField(default=False)),
                ('isAnonymous', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('questionaire_image', models.ImageField(blank=True, upload_to='media')),
                ('is_doctor', models.CharField(blank=True, max_length=5)),
                ('views', models.PositiveBigIntegerField(default=0)),
                ('asked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='QuestionComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('commentor_name', models.CharField(blank=True, max_length=200)),
                ('commentor_image', models.ImageField(blank=True, upload_to='media')),
                ('is_doctor', models.CharField(blank=True, max_length=5)),
                ('comment_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment_feed_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Forum.question')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ArticleLiked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Forum.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Liked Article',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ArticleComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('commentor_name', models.CharField(blank=True, max_length=200)),
                ('is_doctor', models.CharField(blank=True, max_length=5)),
                ('commentor_image', models.ImageField(blank=True, upload_to='media')),
                ('comment_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment_feed_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Forum.article')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Forum.category'),
        ),
    ]
