Follow the [contribution guide](https://github.com/stefan-jansen/alphalens-reloaded/blob/main/CONTRIBUTING.md).
Submit one focused maintenance change. Keep unrelated changes separate.

## Owning issue and change

Closes #

Describe the problem, resulting behavior and compatibility impact. Automated dependency updates
and administrative metadata changes may omit the issue reference; identify that exception here.

Correct verified numerical defects even when existing output changes. For changes to intended
definitions, annualization, sign conventions or defaults, link the agreement in the owning issue.

## Verification

For a bug fix, identify the regression through the affected public API or user workflow.
It must fail because of the defect on the base and pass with the fix, rather than test copied
logic or source text. Record both revisions, commands and results below.

- Base revision, command and failing result:
- Fix revision, command and passing result:
- Other relevant native checks, commands and results:
- Baseline failures, skipped checks or remaining limitations:

Documentation-only changes need rendered documentation and link checks, not an artificial
regression test. For dependency or administrative changes, explain which checks are relevant.

## AI assistance and accountability

State whether AI tools were used, which tools, and which parts they helped produce.

- [ ] I reviewed and tested this submission myself and can explain its code, evidence and responses.
