import secrets

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


CHECK_CHOICES = (
    ("KITCHEN", "Kitchen"),
    ("CLIENT", "Client"),
)


class Printer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=130, unique=True, blank=True)
    check_type = models.CharField(max_length=10, choices=CHECK_CHOICES)
    point_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name


@receiver(pre_save, sender=Printer)
def generate_api_key(sender, instance, **kwargs):
    if not instance.api_key:
        instance.api_key = secrets.token_hex(16)


class Check(models.Model):
    STATUS_CHOICES = (
        ("NEW", "New"),
        ("RENDERED", "Rendered"),
        ("PRINTED", "Printed"),
    )

    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CHECK_CHOICES)
    order = models.JSONField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="NEW"
    )
    pdf_file = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Check - {self.pk}"
