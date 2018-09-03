import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload
import logging

logger = logging.getLogger(__name__)


def restart_celery():
    cmd = 'pkill celery'
    subprocess.call(shlex.split(cmd))
    cmd = '''celery worker
             --app=bitcoin_monitor
             --loglevel=INFO
             --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler'''
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):
    """ management command to run celery using Django's autoreload functionality,
    so that celery will restart upon any code change """

    def handle(self, *args, **options):
        logger.info('Autoreloading celery worker ...')
        autoreload.main(restart_celery)
