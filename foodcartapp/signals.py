from django.dispatch import receiver
from django.db.models import signals

from .models import Order


@receiver(signals.pre_save, sender=Order)
def change_order_status(sender, instance, **kwargs):
    if instance.restaurant is not None and instance.status == 0:
        instance.status = 1


@receiver(signals.pre_save, sender=Order)
def change_order_status(sender, instance, **kwargs):
    if instance.pk is not None:
        old_instance = sender.objects.get(pk=instance.pk)
        if instance.address != old_instance.address:
            print('адрес изменился!')

