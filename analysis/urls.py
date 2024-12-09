from django.urls import path

from analysis.views import TransactionAnalysisViewSet

app_name = "analysis"

urlpatterns = [
    path("analysis/", TransactionAnalysisViewSet.as_view({"post": "create", "get": "list"}), name="analysis")
]
