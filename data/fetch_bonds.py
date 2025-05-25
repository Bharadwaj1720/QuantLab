# data/fetch_bonds.py
import pandas as pd
from datetime import datetime
import pandas_datareader.data as web

# Constant-maturity treasury series for US
FRED_SERIES = {
    "1Y": "DGS1",
    "2Y": "DGS2",
    "5Y": "DGS5",
    "10Y": "DGS10",
    "30Y": "DGS30",
}

def list_us_treasury_tenors():
    """
    Returns the list of available US Treasury constant-maturity tenors.
    """
    return list(FRED_SERIES.keys())


def fetch_us_treasury_yields(
    from_date: str = "2000-01-01",
    to_date: str = None
) -> pd.DataFrame:
    """
    Fetches historical yields for all US Treasury constant-maturity tenors.

    Parameters:
    - from_date: start date in "YYYY-MM-DD" format
    - to_date: end date in "YYYY-MM-DD" format (defaults to today)

    Returns:
    DataFrame indexed by date, columns as tenors (e.g., "1Y", "2Y", ...).
    """
    end = to_date or datetime.today().strftime("%Y-%m-%d")
    df = web.DataReader(list(FRED_SERIES.values()), "fred", from_date, end)
    # Rename columns to tenor labels
    df.rename(columns={v: k for k, v in FRED_SERIES.items()}, inplace=True)
    df.index = pd.to_datetime(df.index)
    # Fill missing values
    df = df.fillna(method="ffill").fillna(method="bfill")
    return df