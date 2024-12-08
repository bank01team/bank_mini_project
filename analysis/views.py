from datetime import datetime
from io import BytesIO

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from analysis.analyzers import TransactionAnalyzer
from analysis.models import Analysis
from analysis.serializers import AnalysisSerializer


class TransactionAnalysisViewSet(ModelViewSet["Analysis"]):
    permission_classes = [IsAuthenticated]
    serializer_class = AnalysisSerializer
    queryset = Analysis.objects.all()
