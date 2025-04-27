# tests/test_calculator.py

import pandas as pd
import pytest
from reliability_metrics.calculator import ReliabilityMetricsCalculator

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'product_name': ['Widget A', 'Widget A', 'Widget B'],
        'ship_month': ['2024-01-01', '2024-02-01', '2024-01-01'],
        'ship_qty': [100, 150, 200],
        'return_month': ['2024-03-01', '2024-04-01', '2024-03-01'],
        'return_qty': [5, 8, 10],
    })

def test_compute_metrics(sample_data):
    calculator = ReliabilityMetricsCalculator(sample_data)
    metrics_df = calculator.compute_metrics()

    # Basic shape check
    assert not metrics_df.empty
    assert 'failure_rate' in metrics_df.columns
    assert 'fit_rate' in metrics_df.columns

    # Check failure rate calculation
    first_row = metrics_df.iloc[0]
    expected_failure_rate = first_row['return_qty'] / first_row['ship_qty']
    assert pytest.approx(first_row['failure_rate'], 0.001) == expected_failure_rate

def test_get_summary(sample_data):
    calculator = ReliabilityMetricsCalculator(sample_data)
    calculator.compute_metrics()
    summary_df = calculator.get_summary()

    assert not summary_df.empty
    assert 'failure_rate' in summary_df.columns
    assert 'fit_rate' in summary_df.columns
