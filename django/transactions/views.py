from rest_framework import viewsets

from transactions.models import Transaction, TransactionInput, TransactionOutput
from transactions.serializers import TransactionInputSerializer, TransactionOutputSerializer, TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # enable case-insensitive partial match
    # filter_backends = [filters.SearchFilter]
    # search_fields = []


class TransactionInputViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """

    queryset = TransactionInput.objects.all()
    serializer_class = TransactionInputSerializer


class TransactionOutputViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """

    queryset = TransactionOutput.objects.all()
    serializer_class = TransactionOutputSerializer
