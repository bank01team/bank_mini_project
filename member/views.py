from dj_rest_auth.jwt_auth import unset_jwt_cookies
from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import Users
from .serializers import RegisterSerializer, UserGetUpdateSerializer, UserSerializer
from .tokens import generate_email_token, send_verification_email


class UserLoginAPI(APIView):
    @swagger_auto_schema(  # type: ignore
        operation_description="로그인 API",
        request_body=openapi.Schema(
            method="post",
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request: Request) -> Response:
        email = request.data["email"]
        password = request.data["password"]

        user = Users.objects.filter(email=email).first()

        if user is None:
            return Response({"message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response({"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)

        token: Token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)  # type: ignore
        refresh_token = str(token)

        response = Response(
            {
                "user": UserSerializer(user).data,
                "message": "login success",
                "token": {"access": access_token, "refresh": refresh_token},
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)
        # 영현 추가
        request.session["user_id"] = user.id
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            refresh_token = request.COOKIES["refresh_token"]
            token = RefreshToken(refresh_token)  # type: ignore
            token.blacklist()
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            unset_jwt_cookies(response)
            return response
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(ModelViewSet[Users]):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UserGetUpdateSerializer

    @swagger_auto_schema(  # type: ignore
        operation_description="Update user's details",
        responses={200: UserGetUpdateSerializer()},
    )
    def partial_update(self, request: Request, **kwargs: bool) -> Response:
        kwargs["partial"] = True
        return super().update(request, **kwargs)

    @swagger_auto_schema(  # type: ignore
        operation_description="Update user's details",
        responses={200: UserGetUpdateSerializer()},
    )
    def update(self, request: Request) -> Response:
        return super().update(request)

    @swagger_auto_schema(  # type: ignore
        operation_description="get user's details",
        responses={200: UserGetUpdateSerializer()},
    )
    def retrieve(self, request: Request) -> Response:
        return super().retrieve(request)

    @swagger_auto_schema(  # type: ignore
        operation_description="delete user'",
        responses={204: openapi.Response(description="No content")},
    )
    def destroy(self, request: Request) -> Response:
        super().destroy(request)
        return Response("Deleted successfully", status=status.HTTP_200_OK)


class RegisterView(ModelViewSet[Users]):
    template_name = "sign_up.html"
    serializer_class = RegisterSerializer

    # @swagger_auto_schema(
    #     operation_description="회원가입 API",
    #     request_body=RegisterSerializer,
    #     responses={201: openapi.Response(description="User registered. Verification email sent.")}
    # )
    def create(self, request: Request) -> Response:

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # 계정 비활성화
            user.email_verification_token = generate_email_token(user)
            user.save()
            send_verification_email(user, request)
            return Response({"message": "User registered. Verification email sent."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateToken(ModelViewSet[Users]):
    @swagger_auto_schema(  # type: ignore
        manual_parameters=[
            openapi.Parameter("token", openapi.IN_QUERY, description="이메일 인증 토큰값", type=openapi.TYPE_STRING)
        ]
    )
    def activate(self, request: Request) -> Response:

        user = Users.objects.get(
            email_verification_token=request.GET["token"]
        )  # 매개변수로 토큰을 받을 수 없음 쿼리파라미터는 받을 수 없음
        if user is not None:
            user.is_active = True
            user.is_email_verified = True
            user.save()
            return Response({"message": "User activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
