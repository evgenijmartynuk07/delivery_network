# Generated by Django 4.2.3 on 2023-07-06 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meal_checks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="check",
            name="pdf_file",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="check",
            name="status",
            field=models.CharField(
                choices=[
                    ("NEW", "new"),
                    ("RENDERED", "rendered"),
                    ("PRINTED", "printed"),
                ],
                default="NEW",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="printer",
            name="api_key",
            field=models.CharField(blank=True, max_length=512, unique=True),
        ),
    ]
