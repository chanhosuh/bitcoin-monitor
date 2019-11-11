from rest_framework import filters, viewsets

from blocks.models import Block
from blocks.serializers import BlockSerializer


class BlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blocks to be viewed or edited.
    """

    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    # enable case-insensitive partial match
    filter_backends = [filters.SearchFilter]
    search_fields = ['height', ]
