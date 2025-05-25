import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def predict_stock_lstm(
    series: pd.Series,
    look_back: int = 60,
    epochs: int = 10,
    future_days: int = 0
) -> pd.DataFrame:
    """
    Train an LSTM on historical price series and optionally forecast future days.

    Parameters:
    - series: pd.Series of closing prices
    - look_back: window length for sequences
    - epochs: number of training epochs
    - future_days: number of days to forecast beyond available data

    Returns DataFrame with columns:
      - 'actual': original series aligned to index
      - 'predicted': in-sample predictions
      - 'forecast': out-of-sample forecasts (NaN for historical dates)
    """
    # Prepare data
    prices = series.dropna().values.reshape(-1,1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices)
    if len(scaled) < look_back + 1:
        raise ValueError("Not enough data for training. Increase the dataset or reduce look_back.")


    # Build sequences
    X, y = [], []
    for i in range(look_back, len(scaled)):
        X.append(scaled[i-look_back:i, 0])
        y.append(scaled[i, 0])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # Define and train model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)),
        LSTM(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=epochs, batch_size=32, verbose=0)

    # In-sample predictions
    preds_scaled = model.predict(X)
    preds = scaler.inverse_transform(preds_scaled)
    predicted = np.concatenate([np.full(look_back, np.nan), preds.flatten()])

    # Future forecasting
    forecast = np.full(len(predicted) + future_days, np.nan)
    forecast[:len(predicted)] = predicted
    if future_days > 0:
        last_seq = scaled[-look_back:]
        seq = last_seq.copy()
        for i in range(future_days):
            inp = seq.reshape((1, look_back, 1))
            f_scaled = model.predict(inp)[0,0]
            seq = np.vstack([seq[1:], [[f_scaled]]])
            f_price = scaler.inverse_transform([[f_scaled]])[0,0]
            forecast[len(predicted) + i] = f_price

    # Build index for forecasted days
    idx = list(series.dropna().index)
    if future_days > 0:
        last_date = idx[-1]
        forecast_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=future_days, freq='B')
        idx = idx + list(forecast_dates)

    # Assemble DataFrame
    df_out = pd.DataFrame({
        'actual': pd.Series(series, index=series.index),
        'predicted': pd.Series(predicted, index=series.index),
    })
    if future_days > 0:
        df_forecast = pd.Series(forecast, index=idx, name='forecast')
        df_out = pd.concat([df_out, df_forecast], axis=1)
    return df_out