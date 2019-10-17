from django.db import models
import pytz
from datetime import datetime
from django.conf import settings


class BolivarControl(object):
    tz = pytz.timezone(settings.TIME_ZONE)
    SOBERANO_CHANGE = 100000.00
    # fechas menores o igual a esta ocurrieron antes del cambio de moneda
    SOBERANO_DATE = datetime(2018, 8, 18, 0, 0, 0, 0, tz)