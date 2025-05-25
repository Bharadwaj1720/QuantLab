# monitoring/model_monitor.py
def monitor_model(actual=None, predicted=None):
    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt

    if actual is None or predicted is None:
        st.info("No data available for monitoring.")
        return

    actual, predicted = np.array(actual), np.array(predicted)
    mask = ~np.isnan(predicted)
    actual, predicted = actual[mask], predicted[mask]

    error = predicted - actual
    mae = np.mean(np.abs(error))
    drift = np.mean(np.gradient(error))

    st.write(f"Mean Absolute Error: {mae:.4f}")
    st.write(f"Mean Drift: {drift:.6f}")

    fig, ax = plt.subplots()
    ax.plot(error)
    ax.set_title("Prediction Error")
    st.pyplot(fig)
