from json import dumps as json_dumps

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard_api.models import (
    Organization,
    CustomUser,
)
from dashboard_api.serializers import (
    RegisterUserSerializer,
)

class TestAPIView(APIView):
    # TODO: don't put this in production
    permission_classes = [AllowAny]

    def get(self, request):
        roles = ["admin", "foo", "bar"]
        new_organization = Organization.objects.create(
            name="Test org",
            roles=json_dumps(roles)
        )

        # new_user = CustomUser.objects.create(
        #     email="abhilaksh@foo.com",
        #     full_name="ASR",
        #     phone_number="000",
        #     organization=new_organization,
        #     role="not_le_admin"
        # )

        return Response({
            'foo': "bar",
        }, status=status.HTTP_200_OK)


class RegisterUserAPIView(APIView):
    """
    Register a new user.
    Method: post
    """

    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    serializer_class = RegisterUserSerializer

    def post(self, request):
        body_serializer = self.serializer_class(data=request.data)
        if not body_serializer.is_valid():
            return Response(body_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = body_serializer.validated_data

        new_user = CustomUser.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            organization_id=validated_data['organization_id'],
            role=validated_data['role']
        )

        return Response({
            'success': True,
            'result': {
                'user_id': new_user.id,
            },
        }, status=status.HTTP_201_CREATED)
