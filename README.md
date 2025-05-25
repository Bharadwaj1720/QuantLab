
# QuantLab Pro

QuantLab Pro is an interactive financial analytics dashboard built with Streamlit. It focuses on quantitative modeling for both fixed income and equity markets.

## 🚀 Features

### US Treasuries (Fixed Income)
- Load and visualize historical US Treasury yield data
- Construct yield curves from par yields
- Bootstrap spot rate curves
- Price zero-coupon bonds using the Hull-White interest rate model
- Simulate interest rate paths using stochastic models

### Stock Analysis
- Load historical stock price data
- Forecast future prices using LSTM neural networks
- Visualize historical trends and model forecasts

### Custom Uploads
- Upload your own bond or stock datasets in CSV format
- View and analyze uploaded data with dynamic charts

## 🧠 Technologies Used
- Python, Streamlit
- Pandas, NumPy, Matplotlib
- Scikit-learn, TensorFlow (LSTM)
- yfinance for market data
- Custom Hull-White implementation

## 📦 Setup

```bash
pip install -r requirements.txt
streamlit run QuantLab/main.py
```

## 🛠 Deployment

Deploy using [Streamlit Cloud](https://streamlit.io/cloud):
- Main file path: `QuantLab/main.py`
- Default branch: `main` or as per your repo
