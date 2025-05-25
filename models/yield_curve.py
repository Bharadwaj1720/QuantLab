import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def plot_yield_curve_on_date(df: pd.DataFrame, date: pd.Timestamp):
    """
    Plots the cross-sectional yield curve for a given date.
    - df: DataFrame with dates as index and bond instruments as columns.
    - date: pandas Timestamp for which to plot the curve.
    """
    # Snap to nearest available date if exact not present
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
        # Parse maturity token (e.g., "10Y", "6M")
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

    # Sort by maturity
    pairs = sorted(zip(maturities, yields))
    x, y = zip(*pairs)

    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_title(f"Yield Curve on {date.date()}")
    ax.set_xlabel("Maturity (Years)")
    ax.set_ylabel("Yield")
    st.pyplot(fig)