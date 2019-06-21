from rest_framework import viewsets

from blocks.models import Block
from blocks.serializers import BlockSerializer


class BlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blocks to be viewed or edited.
    """
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
