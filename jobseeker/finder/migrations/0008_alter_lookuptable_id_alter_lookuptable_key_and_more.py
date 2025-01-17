# Generated by Django 5.1.1 on 2024-10-30 14:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finder", "0007_document"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lookuptable",
            name="id",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="lookuptable",
            name="key",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="lookuptable",
            name="master_key",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="country_code",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="created_by",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="first_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="last_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="modified_by",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="nationality",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="password_hash",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="phone",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user_table",
            name="user_id",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
