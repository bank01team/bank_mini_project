from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from .models import Users
from .serializers import RegisterSerializer
from .tokens import send_verification_email, generate_email_token

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

class RegisterView(ModelViewSet):
    template_name = 'sign_up.html'
    serializer_class = RegisterSerializer
    # @swagger_auto_schema(
    #     operation_description="회원가입 API",
    #     request_body=RegisterSerializer,
    #     responses={201: openapi.Response(description="User registered. Verification email sent.")}
    # )
    def create(self, request):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # 계정 비활성화
            user.email_verification_token = generate_email_token(user)
            user.save()
            send_verification_email(user, request)
            return Response({"message": "User registered. Verification email sent."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateToken(ModelViewSet):
    def activate(self, request):

        user = Users.objects.get(email_verification_token=request.GET["token"]) # 매개변수로 토큰을 받을 수 없음 쿼리파라미터는 받을 수 없음
        if user is not None :
            user.is_active = True
            user.is_email_verified = True
            user.save()
            return Response({"message": "User activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)


# class ProfileView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'profile.html'
#
#     def get(self, request):
#         form = ProfileForm()
#         return Response({'form': form})
#
#     def post(self, request):
#         form = ProfileForm(request.data)
#         if form.is_valid():
#             form.save()
#             return Response({'message': 'success'})
#         return Response({'form': form})[1]


