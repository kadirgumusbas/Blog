# Generated by Django 5.1.6 on 2025-03-07 18:32

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=ckeditor.fields.RichTextField(verbose_name='İçerik'),
        ),
    ]
