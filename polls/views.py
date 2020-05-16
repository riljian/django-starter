from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import DjangoModelPermissions, BasePermission, IsAuthenticated
from rest_framework.decorators import permission_classes, renderer_classes, api_view

from polls.apps import PollsConfig
from polls.models import Poll, PollPermission
from polls.serializers import PollSerializer


class PollSummaryPermission(BasePermission):
    def has_permission(self, request, view):
        permission = f'{PollsConfig.name}.{PollPermission.AGGREGATE_SUMMARY}'
        return request.user.has_perms([permission])


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([PollSummaryPermission])
def aggregate_poll_count(request):
    return Response({'data': Poll.objects.aggregate_count()})


class PollListPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class PollList(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [PollListPermission]
    queryset = Poll.objects.all()

    def get(self, request):
        serializer = PollSerializer(self.queryset.all(), many=True)
        return Response(serializer.data)
