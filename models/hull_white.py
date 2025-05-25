# models/hull_white.py
class HullWhiteModel:
    def __init__(self, a=0.1, sigma=0.01):
        self.a = a
        self.sigma = sigma

    def simulate(self, r0=0.03, T=1.0, dt=0.01):
        import numpy as np
        n = int(T / dt)
        r = [r0]
        for _ in range(1, n):
            dr = self.a * (0.03 - r[-1]) * dt + self.sigma * np.sqrt(dt) * np.random.normal()
            r.append(r[-1] + dr)
        return r

    def run(self):
        import streamlit as st
        import matplotlib.pyplot as plt

        r = self.simulate()
        fig, ax = plt.subplots()
        ax.plot(r)
        ax.set_title("Hull-White Simulation")
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Interest Rate")
        st.pyplot(fig)
