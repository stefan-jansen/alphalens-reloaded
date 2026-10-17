import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from alphalens import performance, tears, utils


@pytest.mark.parametrize("timezone", ["UTC", "US/Eastern"])
def test_timezone_price_workflow_keeps_returns_and_daily_cash_on_supported_pandas(
    timezone,
):
    dates = pd.bdate_range("2025-03-06", periods=12, tz=timezone)
    rates = np.array([0.001, 0.003, 0.006, 0.010])
    prices = pd.DataFrame(
        100 * (1 + rates)[None, :] ** np.arange(12)[:, None],
        index=dates,
        columns=list("abcd"),
    )
    factor = pd.Series(
        np.tile([1.0, 2.0, 3.0, 4.0], 6),
        index=pd.MultiIndex.from_product(
            [dates[:6], list("abcd")], names=["date", "asset"]
        ),
    )
    panel = utils.get_clean_factor_and_forward_returns(
        factor, prices, periods=(1, 2), quantiles=2, filter_zscore=None
    )
    for horizon in (1, 2):
        np.testing.assert_allclose(
            panel[f"{horizon}D"], np.tile((1 + rates) ** horizon - 1, 6), atol=1e-12
        )
    means, _ = performance.mean_return_by_quantile(panel, demeaned=False)
    np.testing.assert_allclose(means["1D"], [0.002, 0.008], atol=1e-12)

    returns, positions, benchmark = performance.create_pyfolio_input(panel, "1D")
    np.testing.assert_allclose(returns.iloc[0], 0, atol=1e-12)
    np.testing.assert_allclose(
        returns, [0, 0.00375, 0, 0, 0.00375, 0.00375, 0.00375, 0.00375], atol=1e-12
    )
    np.testing.assert_allclose(positions.sum(axis=1), 1, atol=1e-12)
    np.testing.assert_allclose(positions.iloc[-1].drop("cash"), 0, atol=1e-12)
    assert positions.iloc[-1]["cash"] == 1
    assert benchmark is not None
    assert returns.index.tz == prices.index.tz

    try:
        tears.create_returns_tear_sheet(panel)
        tears.create_information_tear_sheet(panel)
    finally:
        plt.close("all")
