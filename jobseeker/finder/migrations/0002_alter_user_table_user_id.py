# Generated by Django 5.1.1 on 2024-09-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finder", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_table",
            name="user_id",
            field=models.CharField(primary_key=True, serialize=False),
        ),
    ]