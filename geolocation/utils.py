import logging
import requests
from requests.exceptions import RequestException

from .exceptions import GetCoordinatesException

from .models import Location


logger = logging.getLogger(__name__)


def fetch_coordinates(address, apikey):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()

    found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    if not found_places:
        raise GetCoordinatesException

    most_relevant = found_places[0]['GeoObject']
    lat, lng = most_relevant['Point']['pos'].split(" ")

    return lat, lng


def get_or_create_geopoint(address, apikey):
    address_obj, created = Location.objects.get_or_create(
        address=address,
    )
    if created or address_obj.can_determine_coordinates \
            and address_obj.coordinate_lat is None:
        try:
            lat, lng = fetch_coordinates(address_obj, apikey)
            address_obj.coordinate_lat = lat
            address_obj.coordinate_lng = lng
            address_obj.save()
        except GetCoordinatesException:
            logger.warning(f'Can\'t fetch coordinates for {address_obj}')
            address_obj.can_determine_coordinates = False
            address_obj.save()
        except RequestException:
            logger.warning('Yandex Geo API did not response')
