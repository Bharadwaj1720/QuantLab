import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

class HullWhiteModel:
    def __init__(self, a=0.1, sigma=0.01):
        self.a = a
        self.sigma = sigma

    def simulate(self, r0=0.03, T=1.0, dt=0.01):
        n = int(T / dt)
        r = [r0]
        for _ in range(1, n):
            dr = self.a * (0.03 - r[-1]) * dt + self.sigma * np.sqrt(dt) * np.random.normal()
            r.append(r[-1] + dr)
        return r

    def run(self):
        r = self.simulate()
        fig, ax = plt.subplots()
        ax.plot(r)
        ax.set_title("Hull-White Simulation")
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Interest Rate")
        st.pyplot(fig)

def price_zero_coupon_bond(r0: float, T: float, a: float = 0.1, sigma: float = 0.01) -> float:
    """
    Prices a zero-coupon bond under the Hull-White model using the analytic formula.
    Assumes flat forward rate (theta constant).
    """
    B = (1 - np.exp(-a * T)) / a
    A = np.exp(
        (B - T) * (0.03)**2 / (2 * a**2) -
        (sigma**2) * B**2 / (4 * a)
    )
    return A * np.exp(-B * r0)
