from rest_framework import serializers

from transactions.models import Transaction, TransactionInput, TransactionOutput


class TransactionSerializer(serializers.HyperlinkedModelSerializer):

    vin = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='transactioninput-detail'
    )

    vout = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='transactionoutput-detail'
    )

    class Meta:
        model = Transaction
        fields = (
            "version",
            "locktime",
            "vin",
            "vout",
            "txid",
        )


class TransactionInputSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TransactionInput
        fields = (
            "txid",
            "vout",
            "sequence",
            "script_sig",
        )


class TransactionOutputSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TransactionOutput
        fields = (
            "value",
            "n",
            "script_pubkey",
        )
