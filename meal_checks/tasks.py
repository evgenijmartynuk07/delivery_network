import json
import os
import subprocess

from celery import shared_task
from django.db import transaction
from django.template.loader import render_to_string
from django.conf import settings
from meal_checks.models import Check


@shared_task
def generate_pdf(order_id, printer_id, check_type, order_json) -> str:
    file_name = f"{order_id}_{check_type}.pdf"
    check = Check.objects.get(printer_id=printer_id, order=order_json)

    check_order = json.loads(order_json)["order_details"]

    html_content = render_to_string(
        "check_template.html",
        {
            "order_id": order_id,
            "check_type": check_type,
            "check_order": check_order,
        },
    )

    output_path = os.path.join(settings.MEDIA_ROOT, "pdf", file_name)
    html_file_path = os.path.join(settings.MEDIA_ROOT, "pdf", "input.html")

    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

    docker_host = "localhost"
    port = "8080"

    url = f"http://{docker_host}:{port}/"
    cmd = f'curl -X POST -F "file=@{html_file_path}" {url} -o {output_path}'
    subprocess.run(cmd, shell=True)

    check.status = "RENDERED"
    check.pdf_file.name = f"pdf/{file_name}"
    check.save()

    return f"Check {file_name} created"


@shared_task
def print_generated_check(check_id: int) -> str:
    try:
        check = Check.objects.get(id=check_id)
        with transaction.atomic():
            check.status = "PRINTED"
            check.save()
            return f"Check {check.pdf_file} printed"
    except Check.DoesNotExist:
        return "Check does not exist"


@shared_task
def get_generated_checks() -> None:
    generated_checks = Check.objects.filter(status="RENDERED").all()
    for check in generated_checks:
        print_generated_check.delay(check.id)
