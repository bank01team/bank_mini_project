from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from bank.views import TransactionHistoryView
from member.views import LogoutView, UserLoginAPI, UsersViewSet
from bank.views import AccountViewSet

app_name = "bank"

urlpatterns = [
    path("accounts/", AccountViewSet.as_view({"post": "create", "get": "list"}), name="create-account"),
    path("accounts/<int:pk>", AccountViewSet.as_view({"delete": "destroy"}), name="account-delete"),
    path("transactions/", TransactionHistoryView.as_view({"post": "create", "get": "list"}), name="transactions"),
    path(
        "transactions/<int:id>/",
        TransactionHistoryView.as_view({"put": "update", "delete": "destroy"}),
        name="transactions_id",
    ),
]
