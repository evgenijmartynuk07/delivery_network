from django.db import models

CHECK_CHOICES = (
    ("KITCHEN", "kitchen"),
    ("CLIENT", "client"),
)


class Printer(models.Model):

    name = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=512, unique=True)
    check_type = models.CharField(max_length=10, choices=CHECK_CHOICES)
    point_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Check(models.Model):
    STATUS_CHOICES = (
        ("NEW", "new"),
        ("RENDERED", "rendered"),
        ("PRINTED", "printed"),
    )

    printer_id = models.ForeignKey(Printer, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=10, choices=CHECK_CHOICES)
    order = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    pdf_file = models.FileField()

    def __str__(self) -> str:
        return f"Check - {self.pk}"
