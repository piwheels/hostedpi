import os

from .picloud import PiCloud
from .exc import HostedPiException


HOSTEDPI_ID = os.environ.get('HOSTEDPI_ID')
HOSTEDPI_SECRET = os.environ.get('HOSTEDPI_SECRET')

if API_ID is None or SECRET is None:
    raise HostedPiException('Environment variables HOSTEDPI_ID and HOSTEDPI_SECRET are not set')


def main(args):
    cloud = PiCloud(HOSTEDPI_ID, HOSTEDPI_SECRET)
    
