import math

from stock_universe import (
    STOCK_UNIVERSE,
    RISK_FREE_RATE,
    MARKET_RETURN
)


PAIRWISE_CORRELATION = 0.3
HUMAN_REVIEW_THRESHOLD = 0.20


ALLOCATION_RULES = {
    "Conservative": [
        "PAYBOND",
        "PAYGOLD",
        "PAYRETAIL"
    ],
    "Moderate": [
        "PAYRETAIL",
        "PAYINFRA",
        "PAYGOLD"
    ],
    "Aggressive": [
        "PAYTECH",
        "PAYFIN",
        "PAYINFRA"
    ]
}


def get_stock_data(ticker):
    if ticker not in STOCK_UNIVERSE:
        raise ValueError(f"Unknown ticker: {ticker}")

    return STOCK_UNIVERSE[ticker]


def calculate_capm_return(beta):
    return (
        RISK_FREE_RATE
        + beta * (MARKET_RETURN - RISK_FREE_RATE)
    )


def calculate_portfolio_metrics(tickers):

    weights = {
        ticker: 1 / len(tickers)
        for ticker in tickers
    }

    stock_data = {
        ticker: get_stock_data(ticker)
        for ticker in tickers
    }

    capm_returns = {
        ticker: calculate_capm_return(
            stock_data[ticker]["beta"]
        )
        for ticker in tickers
    }

    portfolio_return = sum(
        weights[ticker] * capm_returns[ticker]
        for ticker in tickers
    )

    variance = 0.0

    # Individual variance
    for ticker in tickers:

        weight = weights[ticker]
        sigma = stock_data[ticker]["std_dev"]

        variance += (
            weight ** 2 * sigma ** 2
        )

    # Pairwise covariance
    for i in range(len(tickers)):

        for j in range(i + 1, len(tickers)):

            ticker_i = tickers[i]
            ticker_j = tickers[j]

            covariance = (
                PAIRWISE_CORRELATION
                * stock_data[ticker_i]["std_dev"]
                * stock_data[ticker_j]["std_dev"]
            )

            variance += (
                2
                * weights[ticker_i]
                * weights[ticker_j]
                * covariance
            )

    portfolio_std = math.sqrt(variance)

    return {
        "tickers": tickers,
        "weights": weights,
        "capm_returns": capm_returns,
        "portfolio_return": portfolio_return,
        "portfolio_variance": variance,
        "portfolio_std": portfolio_std
    }


def mock_recommendation(
    investor_id,
    risk_tolerance,
    tickers,
    portfolio_return,
    portfolio_std
):

    return (
        f"Investor {investor_id} has a "
        f"{risk_tolerance.lower()} risk profile. "
        f"The prescribed portfolio consists of "
        f"{', '.join(tickers)}. "
        f"Estimated CAPM return is "
        f"{portfolio_return:.2%} and estimated "
        f"portfolio volatility is "
        f"{portfolio_std:.2%}."
    )


def advisory_agent(investor):

    investor_id = investor["investor_id"]
    risk_tolerance = investor["risk_tolerance"]

    tickers = ALLOCATION_RULES[risk_tolerance]

    stock_data = {
        ticker: get_stock_data(ticker)
        for ticker in tickers
    }

    metrics = calculate_portfolio_metrics(
        tickers
    )

    portfolio_std = metrics["portfolio_std"]

    if portfolio_std > HUMAN_REVIEW_THRESHOLD:

        decision = "ESCALATED_TO_HUMAN_ADVISOR"
        recommendation = None

    else:

        decision = "AUTO_FINALIZE"

        recommendation = mock_recommendation(
            investor_id,
            risk_tolerance,
            tickers,
            metrics["portfolio_return"],
            portfolio_std
        )

    return {
        "investor_id": investor_id,
        "risk_tolerance": risk_tolerance,
        "tickers": tickers,
        "weights": metrics["weights"],
        "stock_data": stock_data,
        "portfolio_return": metrics["portfolio_return"],
        "portfolio_variance": metrics["portfolio_variance"],
        "portfolio_std": portfolio_std,
        "decision": decision,
        "recommendation": recommendation
    }


def run_all_investors(investors):

    return [
        advisory_agent(investor)
        for investor in investors
    ]
