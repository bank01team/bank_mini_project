from django.urls import path

from bank.views import AccountViewSet

app_name = "bank"

urlpatterns = [
    path("accounts/", AccountViewSet.as_view({"post": "create", "get": "list"}), name="create-account"),
    path("accounts/<int:pk>", AccountViewSet.as_view({"delete": "destroy"}), name="account-delete"),
]
