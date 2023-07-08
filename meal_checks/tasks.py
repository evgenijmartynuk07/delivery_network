import json
import os
import subprocess

from celery import shared_task
from django.db import transaction
from django.template.loader import render_to_string
from django.conf import settings
from meal_checks.models import Check


def create_check_file(file_name: str, html_content: str) -> None:

    media_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf')
    os.makedirs(media_pdf_path, exist_ok=True)

    output_path = os.path.join(media_pdf_path, file_name)
    html_file_path = os.path.join(media_pdf_path, "input.html")

    with open(html_file_path, "w+") as html_file:
        html_file.write(html_content)

    docker_host = "localhost"
    port = "8080"

    url = f"http://{docker_host}:{port}/"
    cmd = f'curl -X POST -F "file=@{html_file_path}" {url} -o {output_path}'
    subprocess.run(cmd, shell=True)


@shared_task
def generate_pdf(
        order_id: int,
        printer_id: int,
        check_type: str,
        order_json: json
) -> str:

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

    create_check_file(file_name=file_name, html_content=html_content)

    with transaction.atomic():
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
