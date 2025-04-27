# src/reliability_metrics/utils.py

from datetime import datetime

def calculate_days_between_months(start_month, end_month):
    """Calculate number of days between two months."""
    start = pd.to_datetime(start_month)
    end = pd.to_datetime(end_month)
    return (end - start).days
