# Generated by Django 4.2.2 on 2023-07-21 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="max_otp_try",),
        migrations.RemoveField(model_name="user", name="otp",),
        migrations.RemoveField(model_name="user", name="otp_expiry",),
        migrations.RemoveField(model_name="user", name="otp_max_out",),
        migrations.RemoveField(model_name="user", name="verified",),
    ]
