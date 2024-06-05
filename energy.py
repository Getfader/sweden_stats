import streamlit as st
from utils.helpers import plotly_line_figure_energy, get_energy_data

def app():
    st.title("Energy production in Sweden")

    fig1 = plotly_line_figure_energy(get_energy_data())
    with st.container():
        st.write("Energy production in Sweden")
        st.plotly_chart(fig1, theme='streamlit', use_container_width=True)