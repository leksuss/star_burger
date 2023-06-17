from rest_framework.serializers import ListField, ModelSerializer
from .models import Order, OrderProduct


class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = ListField(
        child=OrderProductSerializer(),
        allow_empty=False,
    )
    class Meta:
        model = Order
        fields = '__all__'
