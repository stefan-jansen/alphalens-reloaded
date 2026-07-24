#
# Copyright 2017 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd
import pytest

from alphalens.performance import (
    compute_alpha_decay,
    fit_decay_curve,
    factor_decay_half_life,
)


def _make_factor_data(n_dates=120, n_assets=60, periods=(1, 5, 10, 20),
                      decay_half_life=10, seed=42):
    """
    Synthetic factor_data where IC decays with a known half-life.

    Forward return at horizon h: factor * exp(-ln2/hl * h) + noise.
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2020-01-01", periods=n_dates, freq="B")
    assets = [f"A{i:03d}" for i in range(n_assets)]

    idx = pd.MultiIndex.from_product([dates, assets], names=["date", "asset"])
    factor_vals = rng.standard_normal(len(idx))
    factor = pd.Series(factor_vals, index=idx, name="factor")

    lam = np.log(2) / decay_half_life
    fwd_cols = {}
    for h in periods:
        signal = np.exp(-lam * h)
        noise = rng.standard_normal(len(idx)) * 2.0
        fwd_cols[f"{h}D"] = pd.Series(factor_vals * signal + noise, index=idx)

    df = pd.DataFrame({"factor": factor, **fwd_cols})

    def _rank_quantile(x):
        return pd.qcut(x.rank(method="first"), q=5, labels=False) + 1

    df["factor_quantile"] = (
        df.groupby(level="date", group_keys=False)["factor"]
        .transform(_rank_quantile)
        .astype(int)
    )
    return df


class TestComputeAlphaDecay:
    def test_returns_dataframe(self):
        fd = _make_factor_data()
        result = compute_alpha_decay(fd)
        assert isinstance(result, pd.DataFrame)

    def test_index_matches_horizons(self):
        fd = _make_factor_data(periods=(1, 5, 10, 20))
        result = compute_alpha_decay(fd)
        assert list(result.index) == [1, 5, 10, 20]

    def test_required_columns_present(self):
        fd = _make_factor_data()
        result = compute_alpha_decay(fd)
        for col in ("mean_ic", "std_ic", "t_stat", "p_value"):
            assert col in result.columns, f"Missing column: {col}"

    def test_ic_decays_with_horizon(self):
        """IC should be higher at shorter horizons for a decaying factor."""
        fd = _make_factor_data(n_dates=300, n_assets=100,
                               periods=(1, 5, 10, 20), decay_half_life=5)
        result = compute_alpha_decay(fd)
        assert result["mean_ic"].iloc[0] > result["mean_ic"].iloc[-1]

    def test_requires_at_least_two_periods(self):
        fd = _make_factor_data(periods=(5,))
        with pytest.raises(ValueError, match="at least 2"):
            compute_alpha_decay(fd)

    def test_p_values_in_unit_interval(self):
        fd = _make_factor_data()
        result = compute_alpha_decay(fd)
        p = result["p_value"].dropna()
        assert (p >= 0).all() and (p <= 1).all()

    def test_std_ic_nonnegative(self):
        fd = _make_factor_data()
        result = compute_alpha_decay(fd)
        assert (result["std_ic"] >= 0).all()


class TestFitDecayCurve:
    def test_returns_dict_with_required_keys(self):
        fd = _make_factor_data()
        decay_ic = compute_alpha_decay(fd)
        params = fit_decay_curve(decay_ic)
        for key in ("ic0", "lambda_", "half_life", "r_squared", "fit_ok"):
            assert key in params

    def test_recovers_known_half_life(self):
        """Fitted half-life should be within 40% of ground truth."""
        true_hl = 8
        fd = _make_factor_data(n_dates=400, n_assets=150,
                               periods=(1, 3, 5, 8, 10, 15, 20),
                               decay_half_life=true_hl, seed=0)
        decay_ic = compute_alpha_decay(fd)
        params = fit_decay_curve(decay_ic)
        assert params["fit_ok"]
        assert params["half_life"] is not None
        rel_err = abs(params["half_life"] - true_hl) / true_hl
        assert rel_err < 0.40, (
            f"Fitted half-life {params['half_life']:.1f}d deviates "
            f"{rel_err*100:.0f}% from ground truth {true_hl}d"
        )

    def test_handles_non_monotonic_ic_gracefully(self):
        """Should return a dict without raising."""
        bad_ic = pd.DataFrame(
            {"mean_ic": [0.01, 0.05, -0.03, 0.02]},
            index=pd.Index([1, 5, 10, 20], name="horizon"),
        )
        params = fit_decay_curve(bad_ic)
        assert isinstance(params, dict)
        assert "half_life" in params

    def test_half_life_positive_when_fit_ok(self):
        fd = _make_factor_data(n_dates=300, n_assets=100, decay_half_life=10)
        decay_ic = compute_alpha_decay(fd)
        params = fit_decay_curve(decay_ic)
        if params["fit_ok"]:
            assert params["half_life"] > 0


class TestFactorDecayHalfLife:
    def test_returns_float_or_none(self):
        fd = _make_factor_data()
        result = factor_decay_half_life(fd)
        assert result is None or isinstance(result, float)

    def test_positive_for_decaying_factor(self):
        fd = _make_factor_data(n_dates=400, n_assets=150, decay_half_life=10)
        hl = factor_decay_half_life(fd)
        if hl is not None:
            assert hl > 0
