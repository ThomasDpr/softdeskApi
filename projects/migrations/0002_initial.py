# Generated by Django 5.1.4 on 2025-01-17 11:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Auteur'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='projects.issue', verbose_name='Issue associée'),
        ),
        migrations.AddField(
            model_name='project',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_projects', to=settings.AUTH_USER_MODEL, verbose_name='Auteur'),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='projects.project'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributors', to='projects.project'),
        ),
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together={('user', 'project')},
        ),
    ]
