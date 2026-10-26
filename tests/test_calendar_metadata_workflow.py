import numpy as np
import pandas as pd
import pytest
from pandas.tseries.offsets import CustomBusinessDay

from alphalens import performance, utils


def _holiday_inputs(clock, timezone):
    holidays = pd.DatetimeIndex(
        ["2017-01-13", "2017-01-18", "2017-01-30", "2017-02-07"], tz=timezone
    )
    dates = pd.bdate_range("2017-01-12", "2017-02-15", tz=timezone).drop(holidays)
    dates = dates + pd.Timedelta(clock)
    prices = pd.DataFrame(
        100 * np.array([1.1, 0.9])[None, :] ** np.arange(len(dates))[:, None],
        index=dates,
        columns=["a", "b"],
    )
    factor = pd.Series(
        np.tile([1.0, 2.0], len(dates) - 3),
        index=pd.MultiIndex.from_product(
            [dates[:-3], ["a", "b"]], names=["date", "asset"]
        ),
    )
    return factor, prices, holidays


@pytest.mark.parametrize("clock", ["0h", "9h30min"])
@pytest.mark.parametrize("timezone", [None, "America/New_York"])
def test_cleaner_preserves_holiday_frequency_without_mutating_inputs(clock, timezone):
    factor, prices, holidays = _holiday_inputs(clock, timezone)
    original_factor, original_prices = factor.copy(deep=True), prices.copy(deep=True)
    original_frequency = factor.index.levels[0].freq
    forward = utils.compute_forward_returns(
        factor, prices, periods=(1, 2), filter_zscore=None
    )
    supplied = utils.get_clean_factor(factor, forward, quantiles=2)
    composed = utils.get_clean_factor_and_forward_returns(
        factor, prices, periods=(1, 2), quantiles=2, filter_zscore=None
    )
    expected_holidays = tuple(np.datetime64(value.date()) for value in holidays)
    for panel in [forward, supplied, composed, composed.copy(deep=True)]:
        calendar = panel.index.levels[0].freq
        assert isinstance(calendar, CustomBusinessDay)
        assert calendar.weekmask == "Mon Tue Wed Thu Fri"
        assert calendar.holidays == expected_holidays
        pd.testing.assert_index_equal(panel.index, factor.index)
        np.testing.assert_allclose(panel["1D"], np.tile([0.1, -0.1], len(factor) // 2))
        np.testing.assert_allclose(
            panel["2D"], np.tile([0.21, -0.19], len(factor) // 2)
        )
    pd.testing.assert_frame_equal(supplied, composed)
    pd.testing.assert_series_equal(factor, original_factor)
    pd.testing.assert_frame_equal(prices, original_prices)
    assert factor.index.levels[0].freq == original_frequency


@pytest.mark.parametrize("clock", ["0h", "9h30min"])
@pytest.mark.parametrize("group_neutral", [False, True])
@pytest.mark.parametrize("sparse", [False, True])
def test_holiday_cleaner_positions_do_not_expire_on_closed_dates(
    clock, group_neutral, sparse
):
    factor, prices, holidays = _holiday_inputs(clock, None)
    missing_date = pd.Timestamp("2017-01-17") + pd.Timedelta(clock)
    if sparse:
        factor = factor.drop(index=missing_date, level="date")
    panel = utils.get_clean_factor_and_forward_returns(
        factor,
        prices,
        periods=(1,),
        quantiles=2,
        groupby={"a": "sector", "b": "sector"},
        filter_zscore=None,
    )
    positions = performance.factor_positions(panel, "1D", group_neutral=group_neutral)
    weights = performance.factor_weights(panel, group_adjust=group_neutral)
    pd.testing.assert_frame_equal(
        positions,
        performance.positions(weights, "1D", freq=panel.index.levels[0].freq),
    )
    assert not positions.index.normalize().isin(holidays).any()
    factor_dates = factor.index.get_level_values("date").unique()
    np.testing.assert_allclose(
        positions.loc[factor_dates], np.tile([-0.5, 0.5], (len(factor_dates), 1))
    )
    expiry = pd.Timestamp("2017-02-13") + pd.Timedelta(clock)
    if sparse:
        np.testing.assert_array_equal(positions.loc[missing_date], [0.0, 0.0])
    assert positions.index[-1] == expiry
    np.testing.assert_array_equal(positions.loc[expiry], [0.0, 0.0])
