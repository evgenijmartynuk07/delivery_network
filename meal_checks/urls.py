from django.urls import path, include
from rest_framework import routers

from meal_checks.views import OrderCreateView

urlpatterns = [
    path("", OrderCreateView.as_view(), name='order-create'),
]

app_name = "meal_checks"
