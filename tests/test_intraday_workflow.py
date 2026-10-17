import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from alphalens import performance, tears, utils


@pytest.mark.parametrize("indexed_factor", [False, True])
def test_intraday_cleaner_and_summary_preserve_observations_without_zero_day_turnover(
    capsys, indexed_factor
):
    dates = pd.date_range("2025-01-06 09:30", periods=12, freq="h")
    rates = np.array([0.001, 0.003, 0.006, 0.010])
    prices = pd.DataFrame(
        100 * (1 + rates)[None, :] ** np.arange(12)[:, None],
        index=dates,
        columns=list("abcd"),
    )
    factor = pd.DataFrame(
        {
            "date": np.repeat(dates[:6], 4),
            "asset": np.tile(list("abcd"), 6),
            "factor": np.tile([1.0, 2.0, 3.0, 4.0], 6),
        }
    ).set_index(["date", "asset"])["factor"]
    if indexed_factor:
        factor = pd.Series(
            np.tile([1.0, 2.0, 3.0, 4.0], 6),
            index=pd.MultiIndex.from_product(
                [dates[:6], list("abcd")], names=["date", "asset"]
            ),
        )
    original_frequency = factor.index.levels[0].freq
    panel = utils.get_clean_factor_and_forward_returns(
        factor, prices, periods=(1, 2), quantiles=2, filter_zscore=None
    )
    assert factor.index.levels[0].freq == original_frequency
    np.testing.assert_allclose(panel["1h"], np.tile(rates, 6), atol=1e-12)
    np.testing.assert_allclose(
        panel["2h"], np.tile([0.002001, 0.006009, 0.012036, 0.0201], 6), atol=1e-12
    )
    ic = performance.factor_information_coefficient(panel)
    assert ic.index.equals(dates[:6])
    np.testing.assert_allclose(ic, np.ones((6, 2)), atol=1e-12)
    returns = performance.factor_returns(panel, demeaned=False)
    assert returns.index.equals(dates[:6])
    np.testing.assert_allclose(returns["1h"], 0.0065, atol=1e-12)
    np.testing.assert_allclose(returns["2h"], 0.0130527, atol=1e-12)
    persistence = performance.factor_rank_autocorrelation(panel)
    assert persistence.dropna().index.equals(dates[1:6])
    np.testing.assert_allclose(persistence.dropna(), 1, atol=1e-12)
    turnover = performance.quantile_turnover(panel.factor_quantile, 1)
    assert turnover.dropna().index.equals(dates[1:6])
    np.testing.assert_allclose(turnover.dropna(), 0, atol=1e-12)
    try:
        tears.create_summary_tear_sheet(panel)
        assert "0D" not in capsys.readouterr().out
    finally:
        plt.close("all")
