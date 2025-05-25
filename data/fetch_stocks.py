# data/fetch_stocks.py
import pandas as pd
from polygon import RESTClient
from datetime import datetime

API_KEY = "nP9E1Ncua5rLVsP0VN1wNTzbR5KKmYz4"

def fetch_stock_data(symbol: str, start: str = "2000-01-01", end: str = None) -> pd.DataFrame:
    client = RESTClient(API_KEY)
    to_date = end or datetime.today().strftime("%Y-%m-%d")

    try:
        agg_response = client.list_aggs(
            ticker=symbol,
            multiplier=1,
            timespan="day",
            from_=start,
            to=to_date,
            limit=50000
        )
    except Exception as e:
        raise ValueError(f"Failed to fetch data for {symbol}: {e}")

    if not agg_response:
        raise ValueError(f"No data returned for symbol '{symbol}'")

    rows = [{
        "timestamp": a.timestamp,
        "open": a.open,
        "high": a.high,
        "low": a.low,
        "close": a.close,
        "volume": a.volume
    } for a in agg_response]

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    })
    return df[["Open", "High", "Low", "Close", "Volume"]]