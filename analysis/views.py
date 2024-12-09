from datetime import datetime
from io import BytesIO

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from analysis.analyzers import TransactionAnalyzer
from analysis.models import Analysis
from analysis.serializers import AnalysisListSerializer, AnalysisSerializer


class TransactionAnalysisViewSet(ModelViewSet["Analysis"]):
    permission_classes = [IsAuthenticated]
    serializer_class = AnalysisSerializer
    queryset = Analysis.objects.all()

    @swagger_auto_schema(  # type: ignore
        manual_parameters=[
            openapi.Parameter("account", openapi.IN_QUERY, description="계좌 ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter("type", openapi.IN_QUERY, description="weekly or monthly", type=openapi.TYPE_STRING),
            openapi.Parameter(
                "period_start", openapi.IN_QUERY, description="그래프의 시작 날짜", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "period_end", openapi.IN_QUERY, description="그래프의 종료 날짜", type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            account_id=request.GET.get("account"),
            type=request.GET.get("type"),
            period_start=request.GET.get("period_start"),
            period_end=request.GET.get("period_end"),
        )
        if queryset.exists():
            serializer = AnalysisListSerializer(queryset.all(), many=True)
            return Response(serializer.data)
        else:
            for key in request.GET.keys():
                request.data[key] = request.GET.get(key)
            request.data["about"] = f"{request.GET.get("type")}ly balance graph"
            request.data["description"] = f"{request.GET.get("period_start")} to {request.GET.get("period_end")}"
            return self.create(request)
