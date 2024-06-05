import streamlit as st
from age import app as age_app
from health import app as health_app
from energy import app as energy_app
from house import app as house_app

# Dictionary to store the pages and their names
PAGES = {
    "Age Analysis": age_app,
    "Health Analysis": health_app,
    "Energy Analysis": energy_app,
    "House Analysis": house_app
}

def main():
    # Set up the layout
    st.title('Explore Sweden')

    # Navigation dropdown at the top
    selected_page = st.selectbox('Check out another statistic:', list(PAGES.keys()))

    # Run the app function for the selected page
    page = PAGES[selected_page]
    page()

if __name__ == "__main__":
    main()

