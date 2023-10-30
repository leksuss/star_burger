from django.dispatch import receiver
from django.db.models import signals
from django.conf import settings

from geolocation.utils import get_or_create_geopoint

from .models import Order, Restaurant


@receiver(signals.pre_save, sender=Order)
def change_order_status(sender, instance, **kwargs):
    if instance.restaurant is not None and instance.status == 0:
        instance.status = 1


@receiver(signals.pre_save, sender=Order)
@receiver(signals.pre_save, sender=Restaurant)
def get_coordinates_if_needed(sender, instance, **kwargs):
    needed_to_renew_coordinates = False
    if instance.pk is not None:
        old_obj = sender.objects.get(pk=instance.pk)
        if instance.address != old_obj.address:
            needed_to_renew_coordinates = True

    if instance.pk is None or needed_to_renew_coordinates:
        get_or_create_geopoint(instance.address, settings.YANDEX_GEO_API_KEY)
