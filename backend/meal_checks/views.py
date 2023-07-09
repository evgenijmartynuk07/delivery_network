import json
from typing import Optional

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
)
from rest_framework.views import APIView

from .models import Printer, Check
from .serializers import OrderSerializer
from .tasks import generate_pdf


class OrderCreateView(APIView):
    serializer_class = OrderSerializer

    @extend_schema(
        description="""
        Create order.
        1. order_id: It`s unique value for investigate customer.
        2. order_details: Describes what the customer ordered, as well as the price of the order.
        3. point_id: Order location  
        """,
    )
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data["order_id"]
            order_details = serializer.validated_data["order_details"]
            point_id = serializer.validated_data["point_id"]

            printers = Printer.objects.filter(point_id=point_id)

            if not printers.exists():
                return Response(
                    {"error": "Point not found"},
                    status=HTTP_404_NOT_FOUND
                )

            order = {"order_id": order_id, "order_details": order_details}
            order_json = json.dumps(order, cls=DjangoJSONEncoder)

            if Check.objects.filter(order=order_json).exists():
                return Response(
                    {"error": f"Check already exists for order {order_id}"},
                    status=HTTP_409_CONFLICT,
                )

            for printer in printers:
                self.create_sample_check(
                    printer=printer,
                    order_json=order_json,
                    order_id=order_id
                )

            return Response(
                {"message": "Order created"}, status=HTTP_201_CREATED
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def create_sample_check(
            printer: Printer,
            order_json: json,
            order_id: int
    ) -> Optional[Response]:

        try:
            with transaction.atomic():
                check = Check.objects.create(
                    printer_id=printer,
                    type=printer.check_type,
                    order=order_json,
                )
        except Exception as error:
            return Response(
                {"error": f"{error}: Transaction failed"},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

        generate_pdf.delay(
            order_id,
            printer.id,
            check.type,
            order_json
        )
