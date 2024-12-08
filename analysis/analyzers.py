from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth, TruncWeek
from matplotlib.figure import Figure

from bank.models import TransactionHistory


class TransactionAnalyzer:
    def __init__(self, account_id: int):
        self.account_id = account_id

    def get_weekly_data(self, month: int) -> pd.DataFrame:
        transactions = (
            TransactionHistory.objects.filter(
                account_id=self.account_id,
                td_date__month=month,
            )
            .annotate(week=TruncWeek("td_date"))
            .values("week")
            .annotate(daily_balance=Sum("balance"))
            .order_by("week")
        )

        return pd.DataFrame(transactions)

    def get_monthly_data(self, year: int) -> pd.DataFrame:
        transactions = (
            TransactionHistory.objects.filter(
                account_id=self.account_id,
                td_date__year=year,
            )
            .annotate(month=TruncMonth("td_date"))
            .values("month")
            .annotate(daily_balance=Sum("balance"))
            .order_by("month")
        )

        return pd.DataFrame(transactions)

    def plot_weekly_trend(self, month: int) -> Figure:
        df = self.get_weekly_data(month)
        fig = plt.figure(figsize=(10, 5))
        plt.plot(df["week"], df["daily_balance"], marker="o", label="Weekly Balance")
        plt.title("Weekly Transaction Balances")
        plt.xlabel("Week")
        plt.ylabel("Balance")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        return fig

    def plot_monthly_trend(self, year: int) -> Figure:
        df = self.get_monthly_data(year)
        fig = plt.figure(figsize=(10, 5))
        plt.plot(df["month"], df["daily_balance"], marker="o", label="Monthly Balance")
        plt.title("Monthly Transaction Balances")
        plt.xlabel("Month")
        plt.ylabel("Balance")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        return fig
