# Generated by Django 5.1.1 on 2024-10-29 16:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finder", "0006_alter_user_table_created_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("uploaded_file", models.FileField(upload_to="uploads/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]