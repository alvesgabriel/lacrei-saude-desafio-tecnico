from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def home(request):
    data = {'msg': 'Hello World!'}
    return Response(data, status=status.HTTP_200_OK)
