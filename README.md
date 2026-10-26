# pr-reviewer-test

A small demo repository for the
[Autonomous PR Review Swarm](https://github.com/Rishi8603/pr-reviewer).
Every pull request here is reviewed by five AI reviewers (Security, Performance,
Style, QA, Product), and the merge is blocked unless all five approve.

The code is a minimal SQLite wallet (`wallet.py`) plus a calculator
(`calculator.py`), with pytest tests.

## Demo pull requests

| PR | What it changes | Planted problem | Expected result |
|---|---|---|---|
| Transaction history | Records deposits and lists recent ones | None | ✅ 5/5 approve |
| Account search | Search accounts by name | SQL injection, hardcoded admin token logged to stdout | ❌ Security blocks |
| Transfers | Move money between accounts | No check for negative or zero amounts, two separate commits so a failure leaves money missing, no tests | ❌ QA / Performance block |

Open any PR to see the review comment and the `pr-review-swarm` status check.

## Run the tests

```bash
pip install pytest
pytest
```
