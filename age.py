import streamlit as st
from utils.helpers import get_age_data, create_plotly_figure_age

def app():
    st.title("Age Analysis in Sweden")

    fig1 = create_plotly_figure_age(get_age_data())
    with st.container():
       st.write("Exploring age in Sweden")
       st.plotly_chart(fig1, theme='streamlit', use_container_width=True)