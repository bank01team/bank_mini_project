import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
app = Celery("bank_mini_project")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# 스케줄링 설정
app.conf.beat_schedule = {
    "generate-daily-analysis": {
        "task": "analysis.tasks.generate_analysis_report",
        "schedule": crontab(minute="*/1"),  # 매달 말에 실행
    },
}
