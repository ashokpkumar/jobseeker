# Generated by Django 5.1.1 on 2024-09-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finder", "0004_lookuptable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lookuptable",
            name="id",
            field=models.CharField(primary_key=True, serialize=False),
        ),
    ]