from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import json

from dashboard_api.models import (
    Organization,
)

class TestAPIView(APIView):
    # TODO: don't put this in production
    permission_classes = [AllowAny]

    def get(self, request):
        roles = ["foo", "bar"]
        new_organization = Organization.objects.create(
            name="Test org",
            roles=json.dumps(roles)
        )

        return Response({
            'foo': "bar",
        }, status=status.HTTP_200_OK)
    