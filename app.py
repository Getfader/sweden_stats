import streamlit as st
from age import app as age_app
from health import app as health_app
from energy import app as energy_app
from house import app as house_app

# Dictionary to store the pages and their names
PAGES = {
    "Age": age_app,
    "Healthcare": health_app,
    "Energy": energy_app,
    "Apartment Construction": house_app
}

def main():
    # Force wide mode
    st.set_page_config(layout="wide")

    # Navigation dropdown at the top
    selected_page = st.selectbox('Ask a different question:', list(PAGES.keys()))

    # Run the app function for the selected page
    page = PAGES[selected_page]
    page()

if __name__ == "__main__":
    main()
