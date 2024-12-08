from datetime import datetime
from io import BytesIO
from typing import Any

from django.core.files.base import ContentFile
from matplotlib import pyplot as plt
from rest_framework import serializers

from analysis.analyzers import TransactionAnalyzer
from analysis.models import Analysis


class AnalysisSerializer(serializers.ModelSerializer["Analysis"]):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    result_image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Analysis
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data: dict[str, Any]) -> Analysis:
        # bytes를 ContentFile로 변환
        image_bytes = self.get_default_image(validated_data["account"], validated_data["type"])
        validated_data["result_image"] = ContentFile(image_bytes, name=f'analysis_{validated_data["period_start"]}.png')
        return super().create(validated_data)

    def get_default_image(self, account: int, analysis_type: str) -> bytes:
        # self는 시리얼라이저를 가리킴
        analyzer = TransactionAnalyzer(account)
        if analysis_type == "week":
            # 주간 그래프 생성
            fig = analyzer.plot_weekly_trend(month=datetime.now().month)
            weekly_buffer = BytesIO()
            fig.savefig(weekly_buffer, format="png")
            weekly_buffer.seek(0)
            plt.close(fig)
            return weekly_buffer.getvalue()
        else:
            # 월간 그래프 생성
            fig = analyzer.plot_monthly_trend(year=datetime.now().year)
            monthly_buffer = BytesIO()
            fig.savefig(monthly_buffer, format="png")
            monthly_buffer.seek(0)
            plt.close(fig)
            return monthly_buffer.getvalue()
