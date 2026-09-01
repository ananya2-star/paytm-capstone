# Part 3 — AI-Augmented FinTech Advisory & Blockchain Risk

## Objective

This part builds a lightweight AI-assisted advisory toolkit for a hypothetical Paytm Money workflow.

It includes:

- Portfolio advisory using CAPM and portfolio-risk calculations
- Human-in-the-loop escalation
- Structured company-disclosure extraction
- Bull/Bear/Synthesizer multi-agent debate
- DCF valuation and sensitivity analysis
- Blockchain and crypto-risk analysis

---

## Files

- `stock_universe.py` — fictional stock universe with beta, expected return, and volatility
- `investor_profiles.py` — five investor profiles
- `disclosure_snippets.py` — six disclosure examples
- `advisory_agent.py` — portfolio advisory and human-review logic
- `extract_disclosure.py` — structured disclosure-risk extraction
- `debate.py` — Bull, Bear, and Synthesizer agents
- `dcf_calculator.py` — FCFF, WACC, terminal value, sensitivity analysis, and EV/EBITDA comparison
- `blockchain_risk_note.md` — blockchain, crypto, DeFi/DAO, stablecoin, and T.A.N.G. risk analysis

---

## MOCK_LLM Mode

The graded baseline uses deterministic mock logic.

The environment variable is:

`MOCK_LLM`

Default behaviour:

`MOCK_LLM=1`

This means the project runs without any external LLM API, API key, or network call.

The mock path is fully deterministic and is used for the recorded project results.

---

## Portfolio Advisory Agent

The advisory workflow follows three explicit stages:

### THINK

The investor's risk profile is read and mapped to the required portfolio allocation.

### ACT

Stock data is retrieved using `get_stock_data()` and the portfolio's CAPM expected return and portfolio risk are calculated.

### OBSERVE

The resulting portfolio volatility is reviewed.

If portfolio standard deviation exceeds 20%, the recommendation is not automatically finalized and is instead flagged:

`ESCALATED_TO_HUMAN_ADVISOR`

Otherwise, the result is automatically finalized.

---

## Required Portfolio Allocations

### Conservative

Equal-weight allocation across:

- PAYBOND
- PAYGOLD
- PAYRETAIL

### Moderate

Equal-weight allocation across:

- PAYRETAIL
- PAYINFRA
- PAYGOLD

### Aggressive

Equal-weight allocation across:

- PAYTECH
- PAYFIN
- PAYINFRA

Each stock receives a one-third portfolio weight.

---

## Recorded Investor Results

The expected deterministic escalation pattern is:

- INV01 — Conservative — no escalation
- INV02 — Moderate — no escalation
- INV03 — Aggressive — escalated to human advisor
- INV04 — Moderate — no escalation
- INV05 — Aggressive — escalated to human advisor

The aggressive portfolios exceed the 20% volatility threshold and therefore require human review.

---

## CAPM

Expected stock return is calculated using beta only:

`Expected Return = Risk-Free Rate + Beta × (Market Return − Risk-Free Rate)`

The separate `analyst_expected_return` value in the stock universe is not used in the CAPM calculation.

---

## Structured Disclosure Extraction

`extract_disclosure.py` returns:

- `risk_flags`
- `hedging_detected`
- `sentiment`

The deterministic rules detect:

- Litigation risk
- Regulatory risk
- Customer-concentration risk
- Hedging language such as "assuming", "cautiously", and "visibility"
- Confident, cautious, or neutral sentiment

Examples include:

- `doc_02` → litigation risk
- `doc_03` → customer-concentration risk
- `doc_06` → regulatory risk
- `doc_05` → confident sentiment

---

## Multi-Agent Debate

The debate is demonstrated using `PAYTECH`.

Three agents are used:

### Bull Agent

Highlights the expected return and potential upside.

### Bear Agent

Highlights volatility, beta, and downside risk.

### Synthesizer

Combines both perspectives into a balanced conclusion.

The arguments use the actual numeric values stored in `STOCK_UNIVERSE`.

---

## DCF Valuation

The DCF model uses unlevered Free Cash Flow to the Firm:

`FCFF = EBIT × (1 − Tax Rate) + D&A − CapEx − Change in Net Working Capital`

The model includes:

- Base FCFF
- Five-year FCFF projection
- CAPM-based cost of equity
- After-tax cost of debt
- WACC
- Terminal growth rate
- Growing-perpetuity terminal value
- Enterprise value
- 3×3 WACC / terminal-growth sensitivity analysis
- EV/EBITDA cross-check

The sensitivity analysis varies both WACC and terminal growth by ±1 percentage point.

The model verifies that WACC remains greater than terminal growth in every sensitivity cell.

---

## DCF vs EV/EBITDA Comparison

The DCF valuation and EV/EBITDA valuation are used as two different valuation perspectives.

The DCF approach reflects projected future cash flows, growth assumptions, and discount rates, while the EV/EBITDA approach applies a market-style valuation multiple to EBITDA. Therefore, the two values are not expected to be identical. A higher DCF value would suggest that the cash-flow assumptions imply greater long-term value than the multiple-based cross-check, while a lower DCF value would indicate a more conservative cash-flow valuation.

---

## Blockchain and Crypto Risk

See:

`blockchain_risk_note.md`

The note covers:

1. Fiat-backed versus algorithmic stablecoins
2. DeFi and DAO governance risk
3. A specific maximum crypto-allocation recommendation
4. CAPM-based risk reasoning
5. The T.A.N.G. social-engineering framework
6. Two social-engineering vectors
7. A bank-side defense for each vector

---

## How to Run

Run the Part 3 Python files from the `ai_advisory_blockchain` directory.

Example workflow:

1. Run `stock_universe.py`
2. Run `investor_profiles.py`
3. Run `advisory_agent.py`
4. Run `extract_disclosure.py`
5. Run `debate.py`
6. Run `dcf_calculator.py`

No external LLM service is required when `MOCK_LLM=1`.

---

## Design Choices

- CAPM uses beta only, as required.
- Pairwise correlation of 0.3 is used for portfolio-risk calculations.
- Portfolios above 20% volatility are escalated to a human advisor.
- Disclosure extraction uses deterministic keyword/regex rules in mock mode.
- Multi-agent debate uses deterministic templates based on seeded stock values.
- DCF uses a five-year FCFF projection and terminal-value approach.
- Crypto exposure is capped conservatively and treated as a high-risk satellite allocation.

---

## Reproducibility

The Part 3 workflow is deterministic under the default mock mode.

No external API, API key, or network dependency is required for the graded baseline.
