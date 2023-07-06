import asyncio
import os
from asgiref.sync import sync_to_async
from celery import shared_task
import subprocess
from django.template.loader import render_to_string
from django.conf import settings
from meal_checks.models import Check

import threading

lock = threading.Lock()

@shared_task()
def generate_pdf(order_id, check_type, order_json):
    file_name = f"{order_id}_{check_type}.pdf"

    html_content = render_to_string(
        "check_template.html", {
            "order_id": order_id,
            "check_type": check_type,
            "check_order": order_json,
        }
    )
    output_path = os.path.join(settings.MEDIA_ROOT, 'pdf', file_name)
    html_file_path = os.path.join(settings.MEDIA_ROOT, 'pdf', 'input.html')
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)

    docker_host = 'localhost'
    port = '8080'

    url = f"http://{docker_host}:{port}/"
    cmd = f'curl -X POST -F "file=@{html_file_path}" {url} -o {output_path}'
    subprocess.run(cmd, shell=True)

    check = Check.objects.get(order=order_json, type=check_type)
    check.status = "RENDERED"
    check.pdf_file.name = f"pdf/{file_name}"
    check.save()


