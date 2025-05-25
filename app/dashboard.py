import streamlit as st
import pandas as pd
from data.fetch_bonds import list_us_treasury_tenors, fetch_us_treasury_yields
from data.fetch_stocks import fetch_stock_data
from models.yield_curve import plot_yield_curve_on_date
from models.stock_predictor import predict_stock_lstm
from models.hull_white import HullWhiteModel

def run_dashboard():
    st.sidebar.title("QuantLab Pro")
    module = st.sidebar.radio("Select Module", ["US Treasuries", "Stock Analysis"])

    if module == "US Treasuries":
        start = st.sidebar.date_input("From Date", pd.to_datetime("2000-01-01"))
        end = st.sidebar.date_input("To Date", pd.to_datetime("today"))
        if st.sidebar.button("Load Yields"):
            df = fetch_us_treasury_yields(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
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
            plot_yield_curve_on_date(df, pd.to_datetime(date))

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

            st.subheader("Hull-White Simulation on Last Rate")
            HullWhiteModel().run()

    st.sidebar.caption("Built with Streamlit • QuantLab")

if __name__ == "__main__":
    run_dashboard()
