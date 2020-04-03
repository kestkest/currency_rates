import requests
import logging
import datetime

from pytz import utc
from requests.exceptions import HTTPError, ConnectionError, ConnectTimeout
from decimal import Decimal

from defusedxml.ElementTree import fromstring
from django.conf import settings
from django.db import IntegrityError

from .models import Currency


logger = logging.getLogger()


def populate_currency_table():
    try:
        response = requests.get(settings.CURRENCY_RATES_URL)
    except (HTTPError, ConnectionError, ConnectTimeout):
        logger.error("Could not retrieve currency rates document")
        return

    to_insert = []
    data = fromstring(response.content)
    for item in data:
        item_data = item.getchildren()[1:]
        code = item_data[0].text
        nominal = int(item_data[1].text)
        title = item_data[2].text
        rate = Decimal(item_data[3].text.replace(',', '.'))

        to_insert.append(Currency(code=code, nominal=nominal, title=title, rate=rate))

    try:
        Currency.objects.bulk_create(to_insert)
    except IntegrityError:
        logger.warn('Database already populated.')


def update_currency_rates():
    try:
        response = requests.get(settings.CURRENCY_RATES_URL)
    except (HTTPError, ConnectionError, ConnectTimeout):
        logger.error("Could not retrieve currency rates document")
        return

    currencies_map = {c.code: c for c in Currency.objects.all()}
    data = fromstring(response.content)
    now = datetime.datetime.now(tz=utc)

    for item in data:
        item_data = item.getchildren()[1:]
        code = item_data[0].text
        rate = Decimal(item_data[3].text.replace(',', '.'))

        currencies_map[code].rate = rate
        currencies_map[code].updated_at = now

    Currency.objects.bulk_update(currencies_map.values(), ['rate', 'updated_at'])
