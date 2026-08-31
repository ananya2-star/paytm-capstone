import pandas as pd

from stock_universe import (
    STOCK_UNIVERSE,
    RISK_FREE_RATE,
    MARKET_RETURN
)


DCF_ASSUMPTIONS = {
    "ebit_inr": 100_000_000,
    "tax_rate": 0.25,
    "da_inr": 15_000_000,
    "capex_inr": 20_000_000,
    "delta_nwc_inr": 5_000_000,

    "growth_rates": [
        0.12,
        0.10,
        0.08,
        0.07,
        0.06
    ],

    "terminal_growth": 0.05,

    "cost_of_debt": 0.08,

    "equity_weight": 0.70,
    "debt_weight": 0.30,

    "dcf_beta_ticker": "PAYFIN",

    "ebitda_inr": 80_000_000,
    "ev_ebitda_multiple": 10.0
}


def calculate_fcff(
    ebit,
    tax_rate,
    da,
    capex,
    delta_nwc
):
    return (
        ebit * (1 - tax_rate)
        + da
        - capex
        - delta_nwc
    )


def calculate_cost_of_equity(beta):
    return (
        RISK_FREE_RATE
        + beta * (
            MARKET_RETURN
            - RISK_FREE_RATE
        )
    )


def calculate_wacc(
    cost_of_equity,
    cost_of_debt,
    tax_rate,
    equity_weight,
    debt_weight
):
    return (
        equity_weight * cost_of_equity
        + debt_weight
        * cost_of_debt
        * (1 - tax_rate)
    )


def project_fcff(
    base_fcff,
    growth_rates
):

    rows = []
    previous_fcff = base_fcff

    for year, growth in enumerate(
        growth_rates,
        start=1
    ):

        fcff = (
            previous_fcff
            * (1 + growth)
        )

        rows.append({
            "year": year,
            "growth_rate": growth,
            "fcff": fcff
        })

        previous_fcff = fcff

    return pd.DataFrame(rows)


def calculate_terminal_value(
    final_fcff,
    terminal_growth,
    wacc
):

    if wacc <= terminal_growth:
        raise ValueError(
            "WACC must exceed terminal growth."
        )

    return (
        final_fcff
        * (1 + terminal_growth)
        / (wacc - terminal_growth)
    )


def calculate_dcf_value(
    projection,
    terminal_growth,
    wacc
):

    if wacc <= terminal_growth:
        return None

    pv_fcff = sum(
        row["fcff"]
        / (1 + wacc) ** row["year"]
        for _, row in projection.iterrows()
    )

    terminal_value = calculate_terminal_value(
        projection.iloc[-1]["fcff"],
        terminal_growth,
        wacc
    )

    pv_terminal = (
        terminal_value
        / (1 + wacc) ** 5
    )

    return pv_fcff + pv_terminal


def run_dcf():

    a = DCF_ASSUMPTIONS

    beta = STOCK_UNIVERSE[
        a["dcf_beta_ticker"]
    ]["beta"]

    base_fcff = calculate_fcff(
        a["ebit_inr"],
        a["tax_rate"],
        a["da_inr"],
        a["capex_inr"],
        a["delta_nwc_inr"]
    )

    cost_of_equity = calculate_cost_of_equity(
        beta
    )

    wacc = calculate_wacc(
        cost_of_equity,
        a["cost_of_debt"],
        a["tax_rate"],
        a["equity_weight"],
        a["debt_weight"]
    )

    terminal_growth = a["terminal_growth"]

    projection = project_fcff(
        base_fcff,
        a["growth_rates"]
    )

    terminal_value = calculate_terminal_value(
        projection.iloc[-1]["fcff"],
        terminal_growth,
        wacc
    )

    enterprise_value = calculate_dcf_value(
        projection,
        terminal_growth,
        wacc
    )

    ev_ebitda_value = (
        a["ebitda_inr"]
        * a["ev_ebitda_multiple"]
    )

    wacc_values = [
        wacc - 0.01,
        wacc,
        wacc + 0.01
    ]

    growth_values = [
        terminal_growth - 0.01,
        terminal_growth,
        terminal_growth + 0.01
    ]

    sensitivity = pd.DataFrame(
        index=[
            f"{x:.2%}"
            for x in wacc_values
        ],
        columns=[
            f"{x:.2%}"
            for x in growth_values
        ]
    )

    for wacc_value in wacc_values:

        for growth_value in growth_values:

            sensitivity.loc[
                f"{wacc_value:.2%}",
                f"{growth_value:.2%}"
            ] = (
                calculate_dcf_value(
                    projection,
                    growth_value,
                    wacc_value
                )
                / 10_000_000
            )

    worst_case_gap = (
        min(wacc_values)
        - max(growth_values)
    )

    if wacc - terminal_growth < 0.03:
        raise AssertionError(
            "WACC minus terminal growth "
            "is below the required 3% margin."
        )

    if worst_case_gap < 0.01:
        raise AssertionError(
            "Worst-case WACC/growth gap "
            "is below 1%."
        )

    return {
        "base_fcff": base_fcff,
        "beta": beta,
        "cost_of_equity": cost_of_equity,
        "wacc": wacc,
        "terminal_growth": terminal_growth,
        "projection": projection,
        "terminal_value": terminal_value,
        "enterprise_value": enterprise_value,
        "ev_ebitda_value": ev_ebitda_value,
        "sensitivity": sensitivity,
        "worst_case_gap": worst_case_gap
    }
