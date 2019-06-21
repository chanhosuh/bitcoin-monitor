from rest_framework import serializers

from blocks.models import Block


class BlockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Block
        fields = (
            'prev_hash',
            'height',
            'version',
            'merkle_root',
            'timestamp',
            'bits',
            'nonce',
            'num_transactions',
        )
