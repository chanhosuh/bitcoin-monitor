from django.test import TestCase
from django.test.utils import override_settings

from bitcoin_monitor.celery import debug_task


class CeleryTest(TestCase):

    # for testing, globally we've set eager setting to True,
    # so we need to override it for this test
    @override_settings(CELERY_TASK_ALWAYS_EAGER=False)
    def test_debug_task(self):
        """ test celery docker setup is working """
        self.assertTrue(debug_task.delay())
