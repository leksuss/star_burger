import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .models import Order
from .models import OrderProduct


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })

@api_view(['POST'])
def register_order_api(request):
    order = request.data
    if 'products' not in order:
        return Response(
            {'error': 'products is required field'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if order['products'] is None:
        return Response(
            {'error': "products field can\'t be blank or null"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not isinstance(order['products'], list):
        return Response(
            {'error': 'products field should be a list'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not len(order['products']):
        return Response(
            {'error': 'products field should not be blank list'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order_obj = Order.objects.create(
        firstname=order['firstname'],
        lastname=order['lastname'],
        phonenumber=order['phonenumber'],
        address=order['address'],
    )
    for product in order['products']:
        OrderProduct.objects.create(
            order=order_obj,
            product=Product.objects.get(pk=product['product']),
            quantity=product['quantity'],
        )
    return Response({'sucess': 'order registered'})
