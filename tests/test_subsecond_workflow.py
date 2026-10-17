import pandas as pd
import pytest

from alphalens import performance, utils


@pytest.mark.parametrize("period", ["1ns", "1us", "1ms", "1D1ns"])
def test_cleaned_subsecond_returns_are_retained_in_quantile_analysis(period):
    horizon = pd.Timedelta(period)
    dates = pd.date_range("2024-01-01", periods=3, freq=horizon)
    prices = pd.DataFrame({"A": [100, 102, 104], "B": [200, 201, 202]}, index=dates)
    forward = (
        prices.pct_change(fill_method=None)
        .shift(-1)
        .stack()
        .dropna()
        .to_frame(utils.timedelta_to_string(horizon))
    )
    forward.index.names = ["date", "asset"]
    factor = pd.Series([1, 2, 1, 2], index=forward.index)
    clean = utils.get_clean_factor(factor, forward, quantiles=2)
    returns, _ = performance.mean_return_by_quantile(clean, demeaned=False)
    assert returns.loc[1, period] == pytest.approx(
        ((102 / 100 - 1) + (104 / 102 - 1)) / 2
    )
