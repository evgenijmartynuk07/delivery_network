from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    order_details = serializers.CharField()
    point_id = serializers.IntegerField()
