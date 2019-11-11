from rest_framework import serializers

from blocks.models import Block


class BlockSerializer(serializers.HyperlinkedModelSerializer):
    age = serializers.ReadOnlyField()

    transactions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='transaction-detail',
        lookup_field='txid',
    )

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
            'transactions',
            "hash",
            "age",
        )
