"""Check issue #21's unit-gross portfolio through the public tear sheets."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from alphalens import tears, utils


@pytest.mark.parametrize(
    "tear_sheet", [tears.create_summary_tear_sheet, tears.create_returns_tear_sheet]
)
def test_spread_table_matches_half_long_half_short_cash_returns(
    tear_sheet, monkeypatch
):
    plt.switch_backend("Agg")
    dates = pd.date_range("2020-01-02", periods=7)
    prices = pd.DataFrame(
        {
            "asset_a": [10, 11, 10, 12, 10, 11, 13],
            "asset_b": [10, 9, 10, 11, 12, 11, 12],
        },
        index=dates,
    )
    factor = pd.Series(
        [1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2],
        index=pd.MultiIndex.from_product(
            [dates[:-1], prices.columns], names=["date", "asset"]
        ),
    )
    clean = utils.get_clean_factor_and_forward_returns(
        factor, prices, periods=(1,), quantiles=2
    )
    displayed = []
    monkeypatch.setattr(utils, "display", lambda table: displayed.append(table.copy()))
    titles = []
    monkeypatch.setattr(
        plt,
        "show",
        lambda: titles.extend(
            ax.get_title() for num in plt.get_fignums() for ax in plt.figure(num).axes
        ),
    )
    try:
        tear_sheet(clean, long_short=True)
        if tear_sheet is tears.create_returns_tear_sheet:
            assert any("100% gross" in title for title in titles)
    finally:
        plt.close("all")

    # Compute the cash P&L from prices and explicit half-long/half-short holdings.
    daily_asset_returns = prices.to_numpy()[1:] / prices.to_numpy()[:-1] - 1
    weights = np.array(
        [[-0.5, 0.5], [0.5, -0.5], [-0.5, 0.5], [-0.5, 0.5], [0.5, -0.5], [-0.5, 0.5]]
    )
    expected_bps = (daily_asset_returns * weights).sum(axis=1).mean() * 10000
    row = "Mean Period Wise Spread (bps, 100% gross)"
    tables = [table for table in displayed if row in table.index]
    assert len(tables) == 1
    actual_bps = tables[0].loc[row, "1D"]
    print(f"{tear_sheet.__name__}: {actual_bps=}, {expected_bps=}")
    assert actual_bps == pytest.approx(expected_bps, abs=0.0005)
