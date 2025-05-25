def generate_docs():
    import streamlit as st

    doc = """
    # Model Documentation

    ## Yield Curve
    Bootstrapped from treasury rates using linear interpolation.

    ## Hull-White Model
    Simulates short rates with mean reversion (a) and volatility (sigma).

    ## Monitoring
    Tracks MAE and drift in model predictions.

    ## Pricing
    To be implemented: Swaps, Options.
    """

    st.code(doc, language='markdown')