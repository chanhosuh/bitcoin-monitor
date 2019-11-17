import logging
import time

from django.core.management.base import BaseCommand
from django.utils import autoreload

from prices.tasks import update_cc_prices


logger = logging.getLogger(__name__)


WAIT_IN_SECONDS = 10


def _price_feeds():
    while True:
        update_cc_prices.delay()
        time.sleep(WAIT_IN_SECONDS)


class Command(BaseCommand):
    """
    management command to run process using Django's autoreload
    functionality, so that it will restart upon any code change
    """

    def handle(self, *args, **options):
        logger.info("Autoreloading price_feeds ...")
        autoreload.run_with_reloader(_price_feeds)
