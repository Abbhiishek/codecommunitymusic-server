# Generated by Django 4.0 on 2023-09-21 07:14

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_projects_is_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None)),
                ('is_published', models.BooleanField(default=False)),
                ('is_draft', models.BooleanField(default=True)),
                ('appreciators', models.ManyToManyField(blank=True, related_name='appreciated_blogs', to='app.User')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('about', models.TextField(blank=True, default='Welome to new Course of Learning')),
                ('slug', models.TextField(primary_key=True, serialize=False, unique=True)),
                ('is_Active', models.BooleanField(default=True)),
                ('resources', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, default=list, size=None)),
                ('authors', models.ManyToManyField(related_name='course_authors', to='app.User')),
                ('students', models.ManyToManyField(blank=True, related_name='course_students', to='app.User')),
            ],
        ),
        migrations.CreateModel(
            name='SubCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('about', models.TextField(blank=True, default='Welome to new SubCourse of Learning', max_length=200)),
                ('is_Active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='chat',
            name='reply',
        ),
        migrations.AddField(
            model_name='chat',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app.chat'),
        ),
        migrations.AddField(
            model_name='chat',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='forum',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.AlterField(
            model_name='forum',
            name='slug',
            field=models.TextField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='forum',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='upvotes', to='app.User'),
        ),
        migrations.CreateModel(
            name='LearningPath',
            fields=[
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('about', models.TextField(blank=True, default='Welome to new Track of Learning')),
                ('level', models.TextField(blank=True, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=200)),
                ('slug', models.TextField(primary_key=True, serialize=False, unique=True)),
                ('is_Active', models.BooleanField(default=True)),
                ('resources', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, default=list, size=None)),
                ('authors', models.ManyToManyField(related_name='authors', to='app.User')),
                ('courses', models.ManyToManyField(blank=True, related_name='courses', to='app.Course')),
                ('students', models.ManyToManyField(blank=True, related_name='students', to='app.User')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='sub_courses',
            field=models.ManyToManyField(blank=True, related_name='sub_courses', to='app.SubCourse'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.blog')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app.comment')),
            ],
        ),
    ]
