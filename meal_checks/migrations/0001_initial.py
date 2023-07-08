# Generated by Django 4.2.3 on 2023-07-05 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Printer",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("api_key", models.CharField(max_length=512, unique=True)),
                (
                    "check_type",
                    models.CharField(
                        choices=[("KITCHEN", "kitchen"), ("CLIENT", "client")],
                        max_length=10,
                    ),
                ),
                ("point_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Check",
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
                (
                    "type",
                    models.CharField(
                        choices=[("KITCHEN", "kitchen"), ("CLIENT", "client")],
                        max_length=10,
                    ),
                ),
                ("order", models.JSONField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "new"),
                            ("RENDERED", "rendered"),
                            ("PRINTED", "printed"),
                        ],
                        max_length=10,
                    ),
                ),
                ("pdf_file", models.FileField(upload_to="")),
                (
                    "printer_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="meal_checks.printer",
                    ),
                ),
            ],
        ),
    ]