from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from django.db.models import F, Max, Sum, Window
from django.db.models.functions import FirstValue, TruncDate, TruncMonth, TruncWeek
from matplotlib.figure import Figure

from bank.models import TransactionHistory


class TransactionAnalyzer:
    def __init__(self, account_id: int):
        self.account_id = account_id

    def get_weekly_data(self, period_start: datetime, period_end: datetime) -> pd.DataFrame:
        transactions = (
            TransactionHistory.objects.filter(
                account_id=self.account_id,
                td_date__range=(period_start, period_end),
            )
            .annotate(week=TruncWeek("td_date"))
            .values("week")
            .annotate(
                daily_balance=Window(
                    expression=FirstValue("balance"),  # 각 파티션의 첫 번째 값을 선택
                    partition_by=F("week"),  # 주별로 그룹화
                    order_by=F("td_date").desc(),  # 날짜 내림차순 정렬
                )
            )
            .order_by("week")
        )

        return pd.DataFrame(transactions)

    def get_monthly_data(self, period_start: datetime, period_end: datetime) -> pd.DataFrame:
        transactions = (
            TransactionHistory.objects.filter(
                account_id=self.account_id,
                td_date__range=(period_start, period_end),
            )
            .annotate(month=TruncMonth("td_date"))
            .values("month")
            .annotate(
                daily_balance=Window(
                    expression=FirstValue("balance"),  # 각 파티션의 첫 번째 값을 선택
                    partition_by=F("month"),  # 주별로 그룹화
                    order_by=F("td_date").desc(),  # 날짜 내림차순 정렬
                )
            )
            .order_by("month")
        )

        return pd.DataFrame(transactions)

    def plot_weekly_trend(self, period_start: datetime, period_end: datetime) -> Figure:
        df = self.get_weekly_data(period_start, period_end)
        df["week"] = pd.to_datetime(df["week"])
        fig = plt.figure(figsize=(10, 5))
        plt.plot(df["week"], df["daily_balance"], marker="o", label="Weekly Balance")
        plt.title("Weekly Transaction Balances")
        plt.xlabel("Week")
        plt.ylabel("Balance")
        plt.grid(True)
        plt.xticks(df["week"], df["week"].dt.strftime("%Y-%m-%d"), rotation=45)
        plt.legend()
        plt.tight_layout()
        return fig

    def plot_monthly_trend(self, period_start: datetime, period_end: datetime) -> Figure:
        df = self.get_monthly_data(period_start, period_end)
        df["month"] = pd.to_datetime(df["month"])
        fig = plt.figure(figsize=(10, 5))
        plt.plot(df["month"], df["daily_balance"], marker="o", label="Monthly Balance")
        plt.title("Monthly Transaction Balances")
        plt.xlabel("Month")
        plt.ylabel("Balance")
        plt.grid(True)
        plt.xticks(df["month"], df["month"].dt.strftime("%Y-%m-%d"), rotation=45)
        plt.legend()
        plt.tight_layout()
        return fig
