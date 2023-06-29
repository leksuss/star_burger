from django.db import models
from django.utils import timezone

from geopy import distance

class Location(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=255,
        unique=True,
    )
    coordinate_lat = models.FloatField(
        'Широта',
        default=None,
        null=True,
        blank=True,
    )
    coordinate_lng = models.FloatField(
        'Долгота',
        default=None,
        null=True,
        blank=True,
    )
    request_datetime = models.DateTimeField(
        'Время последнего обновления',
        auto_now=True,
        db_index=True,
    )
    can_determine_coordinates = models.BooleanField(
        'Определяются ли координаты адреса',
        default=True,
    )

    def calculate_distance(self, location_obj):
        point1 = self.coordinate_lat, self.coordinate_lng
        point2 = location_obj.coordinate_lat, location_obj.coordinate_lng
        if all([*point1, *point2]):
            return round(distance.great_circle(point1, point2).km, 2)
        return None

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address
