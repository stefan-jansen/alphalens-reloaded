import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402

from alphalens import performance, plotting, utils  # noqa: E402


@pytest.mark.parametrize("bandwidth", [0, 0.5, 2])
@pytest.mark.parametrize("as_frame", [False, True])
def test_spread_plot_honors_error_band_width_from_price_quantiles(bandwidth, as_frame):
    dates = pd.bdate_range("2025-01-06", periods=5)
    rates = np.array([0.001, 0.003, 0.006, 0.010])
    prices = pd.DataFrame(
        100 * (1 + rates)[None, :] ** np.arange(5)[:, None],
        index=dates,
        columns=list("abcd"),
    )
    factor = pd.Series(
        np.tile([1.0, 2.0, 3.0, 4.0], 3),
        index=pd.MultiIndex.from_product(
            [dates[:3], list("abcd")], names=["date", "asset"]
        ),
    )
    panel = utils.get_clean_factor_and_forward_returns(
        factor, prices, periods=(1,), quantiles=2, filter_zscore=None
    )
    means, errors = performance.mean_return_by_quantile(
        panel, by_date=True, demeaned=False
    )
    spread = means.xs(2, level="factor_quantile") - means.xs(1, level="factor_quantile")
    joint_error = np.sqrt(
        errors.xs(2, level="factor_quantile") ** 2
        + errors.xs(1, level="factor_quantile") ** 2
    )
    if not as_frame:
        spread = spread["1D"]
        joint_error = joint_error["1D"]

    try:
        axes = plotting.plot_mean_quantile_returns_spread_time_series(
            spread, std_err=joint_error, bandwidth=bandwidth
        )
        ax = axes[0] if as_frame else axes
        band = ax.collections[0].get_paths()[0].vertices[:, 1]
        np.testing.assert_allclose(
            [band.min(), band.max()],
            [60 - bandwidth * np.sqrt(500), 60 + bandwidth * np.sqrt(500)],
            atol=1e-10,
        )
    finally:
        plt.close("all")
