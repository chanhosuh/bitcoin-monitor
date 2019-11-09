from rest_framework import serializers

from blocks.models import Block


class BlockSerializer(serializers.HyperlinkedModelSerializer):
    hash = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()

    class Meta:
        model = Block
        fields = (
            "prev_hash",
            "height",
            "version",
            "merkle_root",
            "timestamp",
            "bits",
            "nonce",
            "num_transactions",
            "hash",
            "age",
        )
