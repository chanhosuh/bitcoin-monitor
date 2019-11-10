import logging

from django.core.cache import cache
from django.forms.models import model_to_dict

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from blocks.utils import parse_block

from . import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_block(self, raw_block, height):  # pylint: disable=unused-argument
    """
    :param raw_block: string
        hex string for serialized block
    :param height: integer
        height on block chain (genesis block is 0)
    """
    raw_block = bytes.fromhex(raw_block)
    block = parse_block(raw_block, height)

    channel_layer = get_channel_layer()

    last_block = cache.get("block")
    if not last_block or last_block["hash"] != block.hash:
        block_dict = model_to_dict(block)
        block_dict["hash"] = block.hash
        block_dict["age"] = block.age
        cache.set("block", block_dict)
        async_to_sync(channel_layer.group_send)(
            "block", {"type": "block_update", "block": block_dict}
        )
