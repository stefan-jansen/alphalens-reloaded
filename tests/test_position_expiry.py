import pandas as pd
import pytest
from pandas.tseries.offsets import BDay

from alphalens.performance import positions


@pytest.mark.parametrize("days", [3, 4])
def test_weekend_positions_expire_all_coincident_trades_once(days):
    dates = pd.date_range("2024-01-05", periods=days)
    index = pd.MultiIndex.from_product([dates, ["A"]], names=["date", "asset"])
    result = positions(pd.Series(1.0, index=index), "1D", freq=BDay())
    assert result.index.is_unique
    assert (result.loc[dates, "A"] == 1).all()
    assert result.iloc[-1, 0] == 0
    if days == 3:
        assert result.loc[pd.Timestamp("2024-01-08"), "A"] == 0
