import numpy as np
import pandas as pd

import alphalens
from alphalens import performance, utils


assert "site-packages" in alphalens.__file__
np.testing.assert_allclose(
    performance.cumulative_returns(pd.Series([0.1, -0.1])), [1.1, 0.99]
)

dates = pd.bdate_range("2025-01-06", periods=7)
rates = np.array([0.001, 0.002, 0.003, 0.004])
prices = pd.DataFrame(
    100 * (1 + rates)[None, :] ** np.arange(7)[:, None],
    index=dates,
    columns=list("abcd"),
)
factor = pd.DataFrame(
    {
        "date": np.repeat(dates[:4], 4),
        "asset": np.tile(list("abcd"), 4),
        "factor": np.tile([1.0, 2.0, 3.0, 4.0], 4),
    }
).set_index(["date", "asset"])["factor"]
panel = utils.get_clean_factor_and_forward_returns(
    factor, prices, periods=(1,), quantiles=2, filter_zscore=None
)
assert len(panel) == 16
np.testing.assert_allclose(panel["1D"], np.tile(rates, 4), atol=1e-12)
np.testing.assert_allclose(performance.factor_information_coefficient(panel), 1)
np.testing.assert_allclose(
    performance.factor_returns(panel, demeaned=False)["1D"], 0.003, atol=1e-12
)
