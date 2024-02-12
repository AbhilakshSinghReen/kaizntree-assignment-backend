from json import dumps as json_dumps

from rest_framework import generics, mixins, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from dashboard_api.models import (
    Organization,
    CustomUser,
    ItemCategory,
    ItemSubCategory,
    Item,
)
from dashboard_api.serializers import (
    RegisterUserSerializer,
    ItemCategorySerializer,
    ItemSubCategorySerializer,
)

class TestAPIView(APIView):
    # TODO: don't put this in production
    permission_classes = [AllowAny]

    def get(self, request):
        roles = ["admin", "foo", "bar"]
        new_organization_1 = Organization.objects.create(
            name="Org 1",
            roles=json_dumps(roles)
        )

        new_organization_2 = Organization.objects.create(
            name="Org 2",
            roles=json_dumps(roles)
        )

        new_user_1 = CustomUser.objects.create_user(
            email="user1@org1.com",
            username="user1",
            password="1234",
            full_name="User One",
            phone_number="0000000000",
            organization=new_organization_1,
            role="admin"
        )

        new_user_2 = CustomUser.objects.create_user(
            email="user2@org1.com",
            username="user2",
            password="1234",
            full_name="User Two",
            phone_number="0000000000",
            organization=new_organization_1,
            role="admin"
        )

        new_user_3 = CustomUser.objects.create_user(
            email="user3@org2.com",
            username="user3",
            password="1234",
            full_name="User Three",
            phone_number="0000000000",
            organization=new_organization_2,
            role="admin"
        )



        # new_user = CustomUser.objects.create_user(
        #     email="abhilaksh@foo.com",
        #     full_name="ASR",
        #     phone_number="000",
        #     organization=new_organization,
        #     role="not_le_admin"
        # )

        return Response({
            "o1": new_organization_1.id,
            "o2": new_organization_2.id,
            "u1": new_user_1.id,
            "u2": new_user_2.id,
            "u3": new_user_3.id,
        }, status=status.HTTP_200_OK)


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    serializer_class = RegisterUserSerializer

    def post(self, request):
        body_serializer = self.serializer_class(data=request.data)
        if not body_serializer.is_valid():
            return Response(body_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = body_serializer.validated_data

        new_user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            organization=validated_data['organization_id'],
            role=validated_data['role']
        )

        return Response({
            'success': True,
            'result': {
                'user_id': new_user.id,
            },
        }, status=status.HTTP_201_CREATED)


class ItemCategoryGenericAPIView(
        generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin
    ):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ItemCategorySerializer

    queryset = ItemCategory.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(organization=self.request.user.organization)
    
    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        
        return self.list(request)
    
    def post(self, request):
        request.data['organization'] = request.user.organization.id
        return self.create(request)
    
    def put(self, request, id=None):
        request.data['organization'] = request.user.organization.id
        return self.update(request, id)
    
    def delete(self, request, id=None):
        return self.destroy(request, id)
    

class ItemSubCategoryGenericAPIView(
        generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin
    ):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ItemSubCategorySerializer

    queryset = ItemSubCategory.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(organization=self.request.user.organization)

        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category=category_id)
        
        return queryset
    
    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        
        return self.list(request)
    
    def post(self, request):
        request.data['organization'] = request.user.organization.id
        return self.create(request)
    
    def put(self, request, id=None):
        request.data['organization'] = request.user.organization.id
        return self.update(request, id)
    
    def delete(self, request, id=None):
        return self.destroy(request, id)
    




