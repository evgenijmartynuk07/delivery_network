# Generated by Django 4.2 on 2023-07-09 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meal_checks", "0003_alter_check_pdf_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="printer",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
