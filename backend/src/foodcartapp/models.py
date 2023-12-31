from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )
    restaurant = models.ManyToManyField(Restaurant, through='RestaurantMenuItem')

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name='ресторан',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class OrderQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.annotate(
            total_price=Sum(F('order_products__price') * F('order_products__quantity'))
        )

    def unfinished(self):
        return (self.with_total_price()
                    .prefetch_related('products', 'restaurant')
                    .exclude(status=3)
                    .order_by('status'))


class Order(models.Model):
    STATUSES = [
        (0, 'Новый'),
        (1, 'Готовится'),
        (2, 'Доставляется'),
        (3, 'Выполнен'),
    ]
    PAYMENT_TYPES = [
        (0, 'Наличными'),
        (1, 'Электронно'),
        (2, 'Не указан'),
    ]
    firstname = models.CharField(
        'Имя',
        max_length=100,
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=100,
    )
    phonenumber = PhoneNumberField(
        'Телефон',
    )
    address = models.CharField(
        'Адрес',
        max_length=255,
    )
    products = models.ManyToManyField(
        Product,
        through='OrderProduct',
        related_name='orders',
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Готовит ресторан',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    payment_type = models.IntegerField(
        'Способ оплаты',
        choices=PAYMENT_TYPES,
        default=2,
        db_index=True,
    )
    status = models.IntegerField(
        'Статус',
        choices=STATUSES,
        default=0,
        db_index=True,
    )
    comment = models.TextField(
        'Комментарий',
        blank=True,
    )
    registered_at = models.DateTimeField(
        'Заказ создан в',
        default=timezone.now,
        db_index=True,
    )
    called_at = models.DateTimeField(
        'Обратный звонок сделан',
        null=True,
        blank=True,
        db_index=True,
    )
    delivered_at = models.DateTimeField(
        'Доставлено в',
        null=True,
        blank=True,
        db_index=True,
    )

    objects = OrderQuerySet.as_manager()

    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.address}'


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order_products',
        verbose_name='Заказ',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='order_products',
        verbose_name='Товар',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(1)],
    )
    price = models.PositiveIntegerField(
        'Цена',
    )

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары в заказе'
        unique_together = [
            ['order', 'product']
        ]

    def __str__(self):
        return f'Заказ {self.order.id} - {self.product.name}'
