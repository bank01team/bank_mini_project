from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from drf_yasg import openapi

# Create your views here.
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from config.settings.base import REST_FRAMEWORK
from .models import Users
from .serializers import UserGetUpdateSerializer, UserSerializer
from rest_framework.request import Request

class UserLoginAPI(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = Users.objects.filter(username=username).first()

        if user is None:
            return Response({"message": "존재하지 않는 아이디입니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response({"message": "비밀번호가 틀렸습니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        refresh_token = str(token)

        response = Response({
            "user": UserSerializer(user).data,
            "message": "login success",
            "token": {
                "access": access_token,
                "refresh": refresh_token
            }
        }, status=status.HTTP_200_OK)

        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        return response


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# class UsersRegisterViewSet(GenericViewSet):
#     model = Users
#     serializer_class = RegisterSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.data['email']=request.data['email']
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#         #email 인증후  저장


class UsersViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UserGetUpdateSerializer

    @swagger_auto_schema(
        operation_description="Update user's details",
        responses={200: UserGetUpdateSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update user's details",
        responses={200: UserGetUpdateSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="get user's details",
        responses={200: UserGetUpdateSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="delete user'",
        responses={204: openapi.Response(description="No content")},
    )
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response("Deleted successfully",status=status.HTTP_200_OK)


