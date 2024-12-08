from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from analysis.views import TransactionAnalysisViewSet
from bank.views import AccountViewSet, TransactionHistoryView
from member.views import LogoutView, UserLoginAPI, UsersViewSet

app_name = "analysis"

urlpatterns = [
    path("analysis/", TransactionAnalysisViewSet.as_view({"post": "create"}), name="create-analysis"),
]
