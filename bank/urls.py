from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from bank.views import TransactionHistoryView
from member.views import LogoutView, UserLoginAPI, UsersViewSet

app_name = "bank"

urlpatterns = [
    # path(
    #     "users/<int:pk>/",
    #     UsersViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
    # ),
    # path("login/", UserLoginAPI.as_view()),
    path("transactions/", TransactionHistoryView.as_view({"post": "create", "get": "list"}), name="transactions"),
    path(
        "transactions/<int:id>/",
        TransactionHistoryView.as_view({"put": "update", "delete": "destroy"}),
        name="transactions_id",
    ),
]
