from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from member.views import LogoutView, UserLoginAPI, UsersViewSet

app_name = "member"

urlpatterns = [
    path(
        "users/<int:pk>/",
        UsersViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
    ),
    path("login/", UserLoginAPI.as_view()),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
