import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from alphalens import performance, plotting, utils


def test_constant_factor_day_does_not_poison_information_statistics_or_add_zero_ic():
    dates = pd.date_range("2024-01-01", periods=6, freq="B")
    returns = np.array(
        [
            [0.01, 0.02, 0.03],
            [0.01, 0.03, 0.02],
            [0.03, 0.02, 0.01],
            [0.01, 0.02, 0.03],
            [0.02, 0.01, 0.03],
        ]
    )
    prices = pd.DataFrame(
        np.vstack([np.ones(3), np.cumprod(1 + returns, axis=0)]),
        index=dates,
        columns=["A", "B", "C"],
    )
    factor = pd.DataFrame(
        [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 1, 1], [1, 2, 3]],
        index=dates[:-1],
        columns=prices.columns,
    ).stack()
    factor.index.names = ["date", "asset"]
    clean = utils.get_clean_factor_and_forward_returns(
        factor, prices, periods=(1,), quantiles=1
    )
    ic = performance.factor_information_coefficient(clean)
    np.testing.assert_allclose(ic["1D"], [1, 0.5, -1, np.nan, 0.5], equal_nan=True)
    table = plotting.plot_information_table(ic, return_df=True)
    assert table.loc["1D", "t-stat(IC)"] == pytest.approx(1 / np.sqrt(3))
    assert np.isfinite(table.loc["1D", ["p-value(IC)", "IC Skew", "IC Kurtosis"]]).all()
    try:
        _, hist = plt.subplots()
        plotting.plot_ic_hist(ic, ax=[hist])
        assert sum(patch.get_height() for patch in hist.patches) == 4
        _, qq = plt.subplots()
        plotting.plot_ic_qq(ic, ax=[qq])
        assert len(qq.lines[0].get_xdata()) == 4
    finally:
        plt.close("all")
