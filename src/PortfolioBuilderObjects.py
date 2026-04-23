import numpy as np
import pandas as pd
from math_utils import period_to_annual_rate, period_to_annual_sd


class AssetClass:
    """
    Risky asset class.
    Er and sd are annualised and expressed in % form (e.g. 8.5 for 8.5%).
    """

    def __init__(self, name: str, historical_returns: pd.core.series.Series, period: str):
        if not isinstance(historical_returns, pd.core.series.Series):
            raise ValueError("historical_returns must be a pandas Series.")

        self.name = name
        self.historical_returns = historical_returns
        self.period = period
        self.Er = self._compute_er()
        self.sd = self._compute_sd()

    def getName(self):
        return self.name

    def getEr(self):
        return self.Er

    def getSd(self):
        return self.sd

    def _compute_er(self) -> float:
        """Arithmetic mean return, annualised to % form."""
        period_mean = self.historical_returns.mean()
        return period_to_annual_rate(period_mean / 100, self.period)

    def _compute_sd(self) -> float:
        """Sample standard deviation, annualised via square-root-of-time rule."""
        return period_to_annual_sd(self.historical_returns.std(ddof=1), self.period)

    def __str__(self):
        return f"AssetClass = [{self.name}, E(r) = {self.Er:.2f}%, sd = {self.sd:.2f}%]"


class Portfolio:
    """
    Portfolio of AssetClass objects.
    Weights in the composition dict are in % form (e.g. 30.0 for 30%).
    Er and sd are annualised and in % form.
    """

    def __init__(self, name: str, composition: dict, corr_matrix: object):
        self.name = name
        self.color = None
        self.composition = composition
        self.corr_matrix = corr_matrix
        self.Er = self._compute_er()
        self.sd = self._compute_sd()

    def set_color(self, color: str):
        self.color = color

    def _compute_er(self) -> float:
        """
        Er_p = Σ (w_i / 100) * Er_i

        Weights are divided by 100 to convert from % form to fraction.
        """
        return sum((w_i / 100) * a.getEr() for a, w_i in self.composition.items())

    def _compute_sd(self) -> float:
        """
        sd_p = sqrt( ΣΣ (w_i/100)(w_j/100) * corr(i,j) * sd_i * sd_j )
        """
        variance = 0.0
        for asset_i, w_i in self.composition.items():
            for asset_j, w_j in self.composition.items():
                corr = self.corr_matrix[asset_i.getName()][asset_j.getName()]
                variance += (w_i / 100) * (w_j / 100) * corr * asset_i.getSd() * asset_j.getSd()
        return variance ** 0.5

    def _repr_composition(self) -> str:
        lines = ["{\n"]
        for asset_class, w in self.composition.items():
            lines.append(f"    {w:>6.2f}% : {asset_class},\n")
        lines.append("}")
        return "".join(lines)

    def __str__(self):
        return (
            f"Portfolio = [{self.name}, composition = {self._repr_composition()},\n"
            f"E(r) = {self.Er:.2f}%\n"
            f"sd   = {self.sd:.2f}%]"
        )


def convert_portfolios_into_df(portfolios: list) -> pd.DataFrame:
    """
    Input:  list of Portfolio objects
    Output: DataFrame with columns [Name, E(r), sd, Portfolio Object]
    """
    records = [[p.name, p.Er, p.sd, p] for p in portfolios]
    return pd.DataFrame(records, columns=["Name", "E(r)", "sd", "Portfolio Object"])
