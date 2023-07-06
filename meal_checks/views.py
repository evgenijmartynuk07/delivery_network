import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from rest_framework.response import Response
from rest_framework.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from meal_checks.models import Printer, Check, CHECK_CHOICES
from meal_checks.serializers import OrderSerializer
from .tasks import generate_pdf

from delivery_network.celery import debug_task


class OrderCreateView(APIView):

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order_data = {
                'order_id': serializer.validated_data['order_id'],
                'order_details': serializer.validated_data["order_details"],
                'point_id': serializer.validated_data["point_id"],
            }

            printers = Printer.objects.all()

            if not printers.filter(point_id=order_data["point_id"]).exists():
                return Response({"Error: Point not found"}, status=HTTP_404_NOT_FOUND)

            order_json = json.dumps(order_data, cls=DjangoJSONEncoder)

            checks = Check.objects.filter(order=order_json).all()
            if checks.exists():
                return Response({f"Error: Check already exist {order_data['order_id']}"}, status=HTTP_409_CONFLICT)

            printers = printers.filter(point_id=order_data["point_id"])

            check_types = [CHECK_CHOICES[0][1], CHECK_CHOICES[1][1]]
            checks = []

            for printer in printers:
                order_id = order_data["order_id"]

                try:
                    with transaction.atomic():
                        for check_type in check_types:
                            check = Check.objects.create(
                                printer_id=printer,
                                type=check_type,
                                order=order_json,
                            )
                            checks.append(check)
                except Exception as error:
                    return Response({f"{error}: Transaction failed"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

                for check in checks:
                    generate_pdf.delay(order_id, check.type, order_json)

            return Response({"Create"}, status=200)

