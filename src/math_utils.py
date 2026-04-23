DAYS_IN_YEAR   = 365
WEEKS_IN_YEAR  = 52
MONTHS_IN_YEAR = 12
YEARS_IN_YEAR  = 1


def get_num_periods_in_year(period: str) -> int:
    """Returns the number of periods in a year for a given period string."""
    daily   = ["d", "daily", "day"]
    weekly  = ["w", "weekly", "week"]
    monthly = ["m", "monthly", "month"]
    yearly  = ["y", "yearly", "year", "annual"]

    period = period.lower()
    if period in yearly:
        return YEARS_IN_YEAR
    elif period in monthly:
        return MONTHS_IN_YEAR
    elif period in weekly:
        return WEEKS_IN_YEAR
    elif period in daily:
        return DAYS_IN_YEAR
    else:
        print("ERROR: Provided invalid period to get_num_periods_in_year()")
        print("Select from [daily, weekly, monthly, yearly]")
        exit(1)


def period_to_annual_rate(PR: float, period: str) -> float:
    """
    Converts a period rate to annual:
        AR = ((PR + 1)**m - 1) * 100

    PR: period rate in decimal form
    Returns AR in % form (e.g. 8.5 for 8.5%)

    Source: https://www.fool.com/investing/how-to-invest/stocks/how-to-convert-daily-returns-to-annual-returns/
    """
    m = get_num_periods_in_year(period)
    return ((PR + 1) ** m - 1) * 100


def period_to_annual_sd(sd: float, period: str) -> float:
    """
    Converts period standard deviation to annual using the square-root-of-time rule:
        sd_annual = sd_period * sqrt(m)

    Assumes i.i.d. returns.
    """
    m = get_num_periods_in_year(period)
    return sd * m ** 0.5


def convert_tickers_to_AssetClass_obj(composition: dict, asset_classes: list) -> dict:
    """
    Converts a composition dict keyed by ticker strings into one keyed by AssetClass objects.
    """
    ticker_to_obj = {asset.name: asset for asset in asset_classes}
    return {ticker_to_obj[ticker]: weight for ticker, weight in composition.items()}
