# Generated by Django 3.2.9 on 2021-11-09 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='blog_posts', to='blog.blogauthorprofile', verbose_name='author'),
        ),
    ]
