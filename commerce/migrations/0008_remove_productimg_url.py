# Generated by Django 4.2.2 on 2023-08-20 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("commerce", "0007_productimg_image"),
    ]

    operations = [
        migrations.RemoveField(model_name="productimg", name="url",),
    ]
