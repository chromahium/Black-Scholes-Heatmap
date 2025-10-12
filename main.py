from scipy.stats import norm
import math
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def bsop(current, strike, ttm, rfr, vol, round):

    d1 = (math.log(current / strike) + (rfr + vol ** 2 * 0.5) * ttm) / (vol * math.sqrt(ttm))
    
    d2 = d1 - vol * math.sqrt(ttm)

    c = current * norm.cdf(d1) - strike * math.exp(-rfr * ttm) * norm.cdf(d2)

    p = c - current + strike * math.exp(-rfr * ttm)

    return f"{c:.{round}f}", f"{p:.{round}f}"

def generate_ticks(min_tick, max_tick):
    n = 15
    #interval = (max_tick - min_tick) / n - 1
    for i in np.linspace(min_tick, max_tick, int(ticks)):
        yield round(i, 4)

def generate_arrays(vol_min_tick, vol_max_tick, spot_min_tick, spot_max_tick):

    vol_ticks = list(generate_ticks(vol_min_tick, vol_max_tick))    # y-axis
    spot_ticks = list(generate_ticks(spot_min_tick, spot_max_tick)) # x-axis

    bsop_array = []

    for vol_tick in vol_ticks:            # rows = vol (y-axis)
        for spot_tick in spot_ticks:      # columns = spot (x-axis)
            bsop_array.append(bsop(spot_tick, strike_choice, ttm_choice, rfr_choice, vol_tick, 3))

    call__array_values, put_array_values = [], []

    for call_price, put_price in bsop_array:
        call__array_values.append(float(call_price))
        put_array_values.append(float(put_price))

    call_array = np.array(call__array_values)
    call_array = np.reshape(call_array, (len(vol_ticks), len(spot_ticks)))  # rows = vol, cols = spot

    put_array = np.array(put_array_values)
    put_array = np.reshape(put_array, (len(vol_ticks), len(spot_ticks)))

    return call_array, put_array

def get_matrix(show_call=True):
    call_matrix, put_matrix = generate_arrays(min_vol, max_vol, min_spot, max_spot)

    vol_ticks = list(generate_ticks(min_vol, max_vol))
    spot_ticks = list(generate_ticks(min_spot, max_spot))

    vol_ticks = [round(v, 2) for v in generate_ticks(min_vol, max_vol)]
    spot_ticks = [round(s, 2) for s in generate_ticks(min_spot, max_spot)]
  
    fig, ax = plt.subplots()

    if show_call:
        sns.heatmap(call_matrix, annot = True, fmt = ".2f", annot_kws={"size": 6}, ax=ax, cmap="RdYlGn_r",
                    yticklabels=vol_ticks, xticklabels=spot_ticks)
        ax.set_title("Call Option Heatmap")
        ax.tick_params(axis='x', labelrotation=270)
        ax.invert_yaxis()
    else:
        sns.heatmap(put_matrix, annot = True, fmt=".2f", annot_kws={"size": 6}, ax=ax, cmap="RdYlGn_r",
                    yticklabels=vol_ticks, xticklabels=spot_ticks)
        ax.set_title("Put Option Heatmap")
        ax.tick_params(axis='x', labelrotation=270)
        ax.invert_yaxis()

    ax.set(ylabel="Volatility σ", xlabel="Spot Price")

    return fig

def calculate_greeks():
    pass

with st.sidebar:

    st.title("Black-Scholes Option Pricer")
    current_choice = st.number_input("Choose spot price.", min_value=0.01, value = 100.0)
    strike_choice = st.number_input("Choose strike price.", min_value=0.01, value = 80.0)
    ttm_choice = st.number_input("Choose time to maturity.", min_value=0.01, value = 2.0)
    rfr_choice = st.number_input("Choose risk-free rate.", min_value=0.01, value = 0.05)
    vol_choice = st.number_input("Choose volatility.", min_value=0.01, value = 0.1)

    ticks = st.number_input("Ticks", value = 8)

    min_spot = st.number_input("Minimum Spot Price", min_value = 0.01, max_value= current_choice)
    max_spot = st.number_input("Maximum Spot Price", min_value = current_choice)

    min_vol = st.slider("Minimum σ", min_value = 0.0, max_value = 1.0, value = 0.1)
    max_vol = st.slider("Maximum σ", min_value = 0.0, max_value = 1.0, value = 0.3)

call, put = bsop(current_choice, strike_choice, ttm_choice, rfr_choice, vol_choice, 2)

st.metric("Call Price", call)
st.pyplot(get_matrix(True), use_container_width=True)

st.metric("Put Price", put)
st.pyplot(get_matrix(False), use_container_width= True)

