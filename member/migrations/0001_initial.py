# Generated by Django 5.1.3 on 2024-11-29 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone", models.CharField(max_length=50, null=True)),
                ("nickname", models.CharField(max_length=50, null=True)),
                ("password", models.CharField(max_length=255)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("last_login", models.DateTimeField(null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
