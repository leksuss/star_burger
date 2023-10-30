from rest_framework.serializers import ModelSerializer
from .models import Order, OrderProduct


class OrderProductSerializer(ModelSerializer):
    def create(self, validated_data):
        return OrderProduct.objects.create(**validated_data)

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderProductSerializer(
        many=True,
        allow_empty=False,
        write_only=True,
    )

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)

        for product in products:
            OrderProductSerializer().create({
                'order': order,
                'product': product['product'],
                'quantity': product['quantity'],
                'price': product['product'].price,
            })
        return order

    class Meta:
        model = Order
        fields = [
            'id',
            'firstname',
            'lastname',
            'phonenumber',
            'address',
            'products',
        ]
