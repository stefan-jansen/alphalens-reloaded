# Contributing to Alphalens Reloaded

Follow the [shared ML4T contribution policy](https://github.com/ml4t/ecosystem/blob/main/CONTRIBUTING.md).
Alphalens Reloaded accepts bug, security and compatibility fixes. Direct new feature work to
the [current ML4T libraries](https://www.ml4trading.io/).

## Prepare a focused contribution

Search the [issue tracker](https://github.com/stefan-jansen/alphalens-reloaded/issues) first.
Use one issue per problem and discuss substantial changes before implementing them. Include
the affected versions, environment, expected and observed behavior, and a complete minimal
reproduction. Report suspected vulnerabilities through the
[private security process](https://github.com/ml4t/ecosystem/blob/main/SECURITY.md).

Keep each PR focused on its owning issue and include a closing reference such as `Closes #123`.
Automated dependency updates and administrative metadata changes do not require a separate issue.
Keep unrelated fixes, refactors and formatting changes separate; useful fixes from a bundled
submission can be proposed independently.

For a bug fix, exercise the public API or user workflow in a regression. Record the base and fix
revisions, commands and results: the regression must fail because of the defect on the base and
pass with the fix. Tests of copied logic or source text do not establish a behavioral repair.
Documentation changes need documentation checks, not an artificial regression test.

Correct verified numerical defects even when existing output changes. Agree on changes to intended
definitions, annualization, sign conventions or defaults in the owning issue and describe their
compatibility impact.

State whether AI tools helped and identify the affected parts. Review and test your submission
yourself, and be able to explain its code, evidence and review responses. Wait for feedback on
your first focused contribution before opening a large series of similar PRs.

## Run the relevant checks

Use the existing [installation](README.md#installation) and [example usage](README.md#usage)
instructions. From a source checkout, install the development extras and run the checks needed
for the change:

```bash
uv sync --extra test --extra dev --extra docs
uv run pre-commit install
uv run flake8 src tests
uv run pytest tests/
uv run tox
uv run make -C docs html SPHINXOPTS='-W --keep-going'
```

[pyproject.toml](pyproject.toml) defines the extras, pytest configuration and tox environments.
The [test workflow](.github/workflows/unit_tests.yml) defines the CI selection. Tox skips missing
interpreters, so report which environments actually ran. These are Alphalens's native checks;
they do not imply qualification against the current ML4T libraries' support matrix.

For guide or template edits, inspect the rendered Markdown and its links. If the README or Sphinx
sources change, build the documentation and inspect the affected pages. Include exact commands,
results and any baseline limitations in the PR. Existing
[help-wanted issues](https://github.com/stefan-jansen/alphalens-reloaded/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22)
remain a starting point for maintenance contributions.
