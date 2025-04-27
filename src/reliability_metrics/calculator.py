# src/reliability_metrics/calculator.py

import pandas as pd
from .utils import calculate_days_between_months

class ReliabilityMetricsCalculator:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.metrics = None

    def compute_metrics(self):
        df = self.data.copy()

        # Compute days in field
        df['months_in_field'] = df.apply(
            lambda row: calculate_days_between_months(row['ship_month'], row['return_month']) / 30, axis=1)
        df['max_days_in_field'] = df['months_in_field'] * 30

        df['cumulative_shipments'] = df.groupby('product_name')['ship_qty'].cumsum()
        df['cumulative_returns'] = df.groupby('product_name')['return_qty'].cumsum()

        df['failure_rate'] = df['return_qty'] / df['ship_qty']
        df['cumulative_failure_rate'] = df['cumulative_returns'] / df['cumulative_shipments']
        df['mttf'] = df['max_days_in_field']
        df['mtbf'] = df['mttf']
        df['shipments_per_month'] = df['ship_qty']

        df['fit_rate'] = (df['return_qty'] / (df['cumulative_shipments'] * df['max_days_in_field'] * 24)) * 1e9

        self.metrics = df
        return df

    def get_summary(self):
        if self.metrics is None:
            self.compute_metrics()
        return self.metrics.groupby('product_name').mean()
