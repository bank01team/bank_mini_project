from datetime import datetime, timedelta
from io import BytesIO

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.base import ContentFile

from analysis.analyzers import TransactionAnalyzer
from analysis.models import Analysis

logger = get_task_logger(__name__)


@shared_task  # type: ignore
def generate_analysis_report() -> None:
    logger.info("start~~~~~~~~~~~~~~~~~~~~~~~~~")
    """주간/월간 분석 리포트 생성 태스크"""
    analyzer = TransactionAnalyzer(1)

    # 기간 설정
    now = datetime.now()
    period_end = now

    # 주간 분석
    period_start = now - timedelta(weeks=4)
    weekly_plot = analyzer.plot_weekly_trend(period_start, period_end)
    weekly_buffer = BytesIO()
    weekly_plot.savefig(weekly_buffer, format="png")
    weekly_buffer.seek(0)

    Analysis.objects.create(
        user_id=2,
        about="Weekly Analysis",
        type="week",
        period_start=period_start,
        period_end=period_end,
        description="Weekly transaction analysis report",
        result_image=ContentFile(weekly_buffer.getvalue(), name=f'weekly_analysis_{now.strftime("%Y%m%d")}.png'),
        account_id=1,
    )

    # 월간 분석
    period_start = now - timedelta(days=365)
    monthly_plot = analyzer.plot_monthly_trend(period_start, period_end)
    monthly_buffer = BytesIO()
    monthly_plot.savefig(monthly_buffer, format="png")
    monthly_buffer.seek(0)

    Analysis.objects.create(
        user_id=2,
        about="Monthly Analysis",
        type="month",
        period_start=period_start,
        period_end=period_end,
        description="Monthly transaction analysis report",
        result_image=ContentFile(monthly_buffer.getvalue(), name=f'monthly_analysis_{now.strftime("%Y%m%d")}.png'),
        account_id=1,
    )
