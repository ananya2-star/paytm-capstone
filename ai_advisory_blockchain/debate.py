from stock_universe import STOCK_UNIVERSE


def get_stock_data(ticker):
    if ticker not in STOCK_UNIVERSE:
        raise ValueError(f"Unknown ticker: {ticker}")
    return STOCK_UNIVERSE[ticker]


def bull_agent(ticker):

    data = get_stock_data(ticker)

    beta = data["beta"]
    expected_return = data["analyst_expected_return"]
    std_dev = data["std_dev"]

    return (
        f"BULL VIEW — {ticker}: "
        f"The analyst expected return is "
        f"{expected_return:.1%} with a beta of "
        f"{beta:.2f}. This indicates attractive "
        f"potential upside for an investor who can "
        f"tolerate the stock's {std_dev:.1%} volatility."
    )


def bear_agent(ticker):

    data = get_stock_data(ticker)

    beta = data["beta"]
    expected_return = data["analyst_expected_return"]
    std_dev = data["std_dev"]

    return (
        f"BEAR VIEW — {ticker}: "
        f"Although the analyst expected return is "
        f"{expected_return:.1%}, the beta of "
        f"{beta:.2f} and standard deviation of "
        f"{std_dev:.1%} indicate substantial market "
        f"sensitivity and volatility."
    )


def synthesizer_agent(
    ticker,
    bull_argument,
    bear_argument
):

    data = get_stock_data(ticker)

    beta = data["beta"]
    expected_return = data["analyst_expected_return"]
    std_dev = data["std_dev"]

    return (
        f"SYNTHESIS — {ticker}: "
        f"The bull case highlights the "
        f"{expected_return:.1%} expected return, "
        f"while the bear case highlights the "
        f"{beta:.2f} beta and {std_dev:.1%} volatility. "
        f"Overall, the stock may offer attractive "
        f"upside but is more appropriate for investors "
        f"who can tolerate substantial fluctuations."
    )


def run_debate(ticker="PAYTECH"):

    bull = bull_agent(ticker)
    bear = bear_agent(ticker)

    synthesis = synthesizer_agent(
        ticker,
        bull,
        bear
    )

    return {
        "ticker": ticker,
        "bull_argument": bull,
        "bear_argument": bear,
        "synthesis": synthesis
    }
