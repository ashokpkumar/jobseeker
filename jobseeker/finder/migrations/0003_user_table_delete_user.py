# Generated by Django 5.1.1 on 2024-09-20 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finder", "0002_alter_user_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="User_table",
            fields=[
                ("user_id", models.IntegerField(primary_key=True, serialize=False)),
                ("first_name", models.CharField()),
                ("last_name", models.CharField()),
                ("gender", models.IntegerField()),
                ("nationality", models.CharField()),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField()),
                ("country_code", models.CharField()),
                ("user_type", models.IntegerField()),
                ("created_by", models.IntegerField()),
                ("created_time", models.DateTimeField()),
                ("modified_by", models.IntegerField()),
                ("modified_time", models.DateTimeField()),
                ("hidden", models.BooleanField()),
                ("password_hash", models.CharField())
            ],
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]