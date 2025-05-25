import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_yield_curve_on_date(df: pd.DataFrame, date: pd.Timestamp):
    """
    Plots the cross-sectional yield curve for a given date.
    - df: DataFrame with dates as index and bond instruments as columns.
    - date: pandas Timestamp for which to plot the curve.
    """
    if date not in df.index:
        available = df.index[df.index <= date]
        if available.empty:
            st.error(f"No yield data on or before {date.date()}")
            return
        date = available.max()

    row = df.loc[date].dropna()
    maturities = []
    yields = []
    for col, val in row.items():
        token = col.split()[-1]
        try:
            if token.endswith('Y'):
                m = float(token[:-1])
            elif token.endswith('M'):
                m = float(token[:-1]) / 12
            else:
                continue
            maturities.append(m)
            yields.append(val)
        except Exception:
            continue

    if not maturities:
        st.error("No maturities parsed for this date.")
        return

    pairs = sorted(zip(maturities, yields))
    x, y = zip(*pairs)

    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_title(f"Yield Curve on {date.date()}")
    ax.set_xlabel("Maturity (Years)")
    ax.set_ylabel("Yield")
    st.pyplot(fig)

def bootstrap_yield_curve(yields: pd.Series) -> pd.Series:
    """
    Bootstraps spot rates from a par yield curve (simple annual coupon assumption).
    Only valid for demonstration and assumes tenors labeled like '1Y', '2Y', ...
    """
    spot_rates = []
    tenors = []
    for i, (label, coupon) in enumerate(yields.items()):
        try:
            if label.endswith("Y"):
                t = int(label[:-1])
            elif label.endswith("M"):
                t = float(label[:-1]) / 12
            else:
                continue
            tenors.append(label)
        except Exception:
            continue

        if i == 0:
            spot = coupon / 100
        else:
            sum_pv = sum([(coupon / 100) / (1 + spot_rates[j]) ** (j + 1) for j in range(i)])
            spot = ((1 + coupon / 100) / (1 - sum_pv)) ** (1 / (i + 1)) - 1
        spot_rates.append(spot)

    series = pd.Series(spot_rates, index=tenors)
    return series.sort_index(key=lambda idx: [float(i[:-1]) if i.endswith("Y") else float(i[:-1])/12 for i in idx])


    


def sort_columns_by_maturity(columns):
    def get_maturity(col):
        try:
            if col.endswith('Y'):
                return float(col[:-1])
            elif col.endswith('M'):
                return float(col[:-1]) / 12
        except:
            return float('inf')
    return sorted(columns, key=get_maturity)
