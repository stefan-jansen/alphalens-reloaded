<p align="center">
<a href="https://alphalens.ml4trading.io">
<img src="https://i.imgur.com/uf8PmQO.png" width="35%">
</a>
</p>

![PyPI](https://img.shields.io/pypi/v/alphalens-reloaded)
![Conda](https://img.shields.io/conda/pn/ml4t/alphalens-reloaded)
[![Tests](https://github.com/stefan-jansen/alphalens-reloaded/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/stefan-jansen/alphalens-reloaded/actions/workflows/unit_tests.yml)
[![PyPI Wheels](https://github.com/stefan-jansen/alphalens-reloaded/actions/workflows/distribution.yml/badge.svg)](https://github.com/stefan-jansen/alphalens-reloaded/actions/workflows/distribution.yml)
[![Alphalens conda distribution](https://github.com/stefan-jansen/alphalens-reloaded/actions/workflows/conda_package.yml/badge.svg)](https://github.com/stefan-jansen/alphalens-reloaded/actions/workflows/conda_package.yml)
[![Coverage Status](https://coveralls.io/repos/github/stefan-jansen/alphalens-reloaded/badge.svg?branch=main)](https://coveralls.io/github/stefan-jansen/alphalens-reloaded?branch=main)
![GitHub issues](https://img.shields.io/github/issues/stefan-jansen/alphalens-reloaded)
![PyPI - License](https://img.shields.io/pypi/l/alphalens-reloaded)
![Discourse users](https://img.shields.io/discourse/users?server=https%3A%2F%2Fexchange.ml4trading.io%2F)
![Twitter Follow](https://img.shields.io/twitter/follow/ml4trading?style=social)

Alphalens is a Python library for performance analysis of predictive
(alpha) stock factors. Alphalens works great with the
[Zipline](https://www.zipline.ml4trading.io/) open source backtesting library, and [Pyfolio](https://github.com/quantopian/pyfolio) which provides performance and risk analysis of financial portfolios.

The main function of Alphalens is to surface the most relevant statistics and plots about an alpha factor, including:

- Returns Analysis
- Information Coefficient Analysis
- Turnover Analysis
- Grouped Analysis

# Getting started

With a signal and pricing data creating a factor \"tear sheet\" is a two step process:

```python
import alphalens

# Ingest and format data
factor_data = alphalens.utils.get_clean_factor_and_forward_returns(my_factor,
                                                                   pricing,
                                                                   quantiles=5,
                                                                   groupby=ticker_sector,
                                                                   groupby_labels=sector_names)

# Run analysis
alphalens.tears.create_full_tear_sheet(factor_data)
```

# Learn more

Check out the [example notebooks](https://github.com/stefan-jansen/alphalens-reloaded/tree/master/alphalens/examples)
for more on how to read and use the factor tear sheet.

# Installation

Install with pip:

    pip install alphalens-reloaded

Install with conda:

    conda install -c ml4t alphalens-reloaded

Install from the master branch of Alphalens repository (development code):

    pip install git+https://github.com/stefan-jansen/alphalens-reloaded

Alphalens depends on:

- [matplotlib](https://github.com/matplotlib/matplotlib)
- [numpy](https://github.com/numpy/numpy)
- [pandas](https://github.com/pandas-dev/pandas)
- [scipy](https://github.com/scipy/scipy)
- [seaborn](https://github.com/mwaskom/seaborn)
- [statsmodels](https://github.com/statsmodels/statsmodels)

# Usage

A good way to get started is to run the examples in a [Jupyter notebook](https://jupyter.org/).

To get set up with an example, you can:

Run a Jupyter notebook server via:

```bash
jupyter notebook
```

From the notebook list page(usually found at `http://localhost:8888/`), navigate over to the examples directory, and open any file with a .ipynb extension.

Execute the code in a notebook cell by clicking on it and hitting Shift+Enter.

# Questions?

If you find a bug, feel free to open an issue on our [github tracker](https://github.com/stefan-jansen/alphalens-reloaded/issues).

# Contribute

If you want to contribute, a great place to start would be the
[help-wanted issues](https://github.com/stefan-jansen/alphalens-reloaded/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22).

# Credits

- [Andrew Campbell](https://github.com/a-campbell)
- [James Christopher](https://github.com/jameschristopher)
- [Thomas Wiecki](https://github.com/twiecki)
- [Jonathan Larkin](https://github.com/marketneutral)
- Jessica Stauth (<jstauth@quantopian.com>)
- [Taso Petridis](https://github.com/tasopetridis)

For a full list of contributors see the [contributors page.](https://github.com/stefan-jansen/alphalens-reloaded/graphs/contributors)

# Example Tear Sheets

Example factor courtesy of [ExtractAlpha](https://extractalpha.com/)

## Peformance Metrics Tables

![image](https://i.imgur.com/4T8cziG.png)

## Returns Tear Sheet

![image](https://i.imgur.com/aVs3KiM.png)

## Information Coefficient Tear Sheet

![image](https://i.imgur.com/vAm8okb.png)

## Sector Tear Sheet

![image](https://i.imgur.com/pnBs0ta.png)
