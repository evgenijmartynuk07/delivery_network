from django.urls import path

from meal_checks.views import OrderCreateView

urlpatterns = [
    path("", OrderCreateView.as_view(), name="order-create"),
]

app_name = "meal_checks"
