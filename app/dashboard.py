import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data.fetch_bonds import list_us_treasury_tenors, fetch_us_treasury_yields
from data.fetch_stocks import fetch_stock_data
from models.yield_curve import plot_yield_curve_on_date, bootstrap_yield_curve, sort_columns_by_maturity
from models.stock_predictor import predict_stock_lstm
from models.hull_white import HullWhiteModel, price_zero_coupon_bond

# Dashboard Entry Point

import pandas as pd
from data.fetch_bonds import list_us_treasury_tenors, fetch_us_treasury_yields
from data.fetch_stocks import fetch_stock_data
from models.yield_curve import plot_yield_curve_on_date, bootstrap_yield_curve, sort_columns_by_maturity
from models.stock_predictor import predict_stock_lstm
from models.hull_white import HullWhiteModel, price_zero_coupon_bond

def run_dashboard():
    st.sidebar.title("QuantLab")
    module = st.sidebar.radio("Select Module", ["Home", "US Treasuries", "Stock Analysis"])

    if module == "Home":
        st.title("Welcome to QuantLab")
        st.markdown("""
        ### Features:
        - **US Treasuries:** Load and visualize historical US Treasury yields, construct yield curves, and price zero-coupon bonds using the Hull-White model.
        - **Stock Analysis:** Load market data for any stock, apply LSTM for future price prediction, and visualize historical trends.
        - **Upload CSV:** Upload your own bond or stock datasets for visualization.
        - **Risk-Neutral Valuation:** Bond pricing using Hull-White interest rate model.
        - **Yield Curve Construction:** Spot rate bootstrapping from par yields.
        """)

    elif module == "US Treasuries":
        start = st.sidebar.date_input("From Date", pd.to_datetime("2000-01-01"))
        end = st.sidebar.date_input("To Date", pd.to_datetime("today"))
        if st.sidebar.button("Load Yields"):
            df = fetch_us_treasury_yields(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
            df = df[sort_columns_by_maturity(df.columns)]
            st.session_state['yield_df'] = df

        if 'yield_df' in st.session_state:
            df = st.session_state['yield_df']
            st.subheader("US Treasury Yield Time Series")
            st.line_chart(df)
            date = st.slider(
                "Curve Date",
                min_value=df.index.min().date(),
                max_value=df.index.max().date(),
                value=df.index.max().date(),
                format="YYYY-MM-DD"
            )

            st.subheader("Yield Curve Construction")
            selected_date = pd.to_datetime(date)
            available = df.index[df.index <= selected_date]
            if available.empty:
                st.error(f"No yield data available on or before {selected_date.date()}")
                return
            spot_rates = bootstrap_yield_curve(df.loc[available.max()])
            # Plot spot curve with correct numeric ordering
            fig, ax = plt.subplots()
            maturities = [float(t[:-1]) if t.endswith('Y') else float(t[:-1])/12 for t in spot_rates.index]
            rates = spot_rates.values
            ax.plot(maturities, rates, marker='o')
            ax.set_xticks(maturities)
            ax.set_xticklabels(spot_rates.index)
            ax.set_xlabel('Maturity (Years)')
            ax.set_ylabel('Spot Rate')
            ax.set_title(f"Spot Rate Curve on {available.max().date()}")
            st.pyplot(fig)

            st.subheader("Zero-Coupon Bond Pricing (Hull-White)")
            r0 = df.loc[available.max()].iloc[-1] / 100
            maturity = st.slider("Maturity (Years)", 1, 30, 10)
            price = price_zero_coupon_bond(r0, maturity)
            st.write(f"Bond Price (T={maturity}): {price:.4f}")

    else:
        ticker = st.sidebar.text_input("Ticker (e.g., AAPL)").upper()
        start = st.sidebar.date_input("Start Date", pd.to_datetime("2010-01-01"))
        end = st.sidebar.date_input("End Date", pd.to_datetime("today"))
        future = st.sidebar.number_input("Forecast Days", min_value=0, value=0)
        if ticker and st.sidebar.button("Load Stock Data"):
            try:
                df = fetch_stock_data(ticker, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
                st.session_state['stock_df'] = df
                st.session_state['stock_error'] = None
            except Exception as e:
                st.session_state['stock_error'] = str(e)

        if st.session_state.get('stock_error'):
            st.error(st.session_state['stock_error'])
        elif 'stock_df' in st.session_state:
            df = st.session_state['stock_df']
            st.subheader(f"{ticker} Price History")
            st.line_chart(df['Close'])

            st.subheader("LSTM Forecast")
            try:
                result = predict_stock_lstm(df['Close'], look_back=60, epochs=10, future_days=future)
                plot_df = result[['actual']].copy()
                if 'forecast' in result.columns and result['forecast'].notna().sum() > 0:
                    plot_df['forecast'] = result['forecast']
                st.line_chart(plot_df)
            except Exception as e:
                st.error(f"Forecasting failed: {e}")

            

    st.sidebar.caption("Built with Streamlit • QuantLab")

    # Optional upload for user-provided data
    st.sidebar.markdown("---")
    st.sidebar.subheader("Upload Custom Data")

    uploaded_bond = st.sidebar.file_uploader("Upload Bond Data (CSV)", type="csv", key="user_bond")
    if uploaded_bond:
        user_df = pd.read_csv(uploaded_bond, index_col=0, parse_dates=True)
        st.subheader("Custom Bond Data")
        st.dataframe(user_df)
        st.line_chart(user_df)

    uploaded_stock = st.sidebar.file_uploader("Upload Stock Data (CSV)", type="csv", key="user_stock")
    if uploaded_stock:
        user_df = pd.read_csv(uploaded_stock, index_col=0, parse_dates=True)
        st.subheader("Custom Stock Data")
        st.line_chart(user_df)

if __name__ == "__main__":
    run_dashboard()
