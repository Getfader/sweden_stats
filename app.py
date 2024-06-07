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
    "Apartments": house_app
}

def sidebar():
    """
    Define the content for the sidebar.

    This function sets up the content displayed in the sidebar of the Streamlit app.
    It includes the title, welcome message, a brief description, and a link to the data source.

    Returns:
        None
    """
    st.sidebar.title("Sweden Stats Dashboard")
    st.sidebar.markdown("Welcome to Sweden Stats!")
    st.sidebar.markdown("Explore different datasets related to Sweden.")
    st.sidebar.markdown("Select a dashboard from the dropdown on the top to get started.")
    st.sidebar.markdown("[Data Source](https://www.statistikdatabasen.scb.se/pxweb/en/ssd/)")

def main():
    """
    Main function to set up the Sweden Stats Dashboard.

    This function configures the Streamlit app layout and handles navigation.
    It sets up the sidebar content and a dropdown menu for selecting different dashboards.
    Based on the selected dashboard, it runs the corresponding app function.

    Returns:
        None
    """
    # Force wide mode
    st.set_page_config(layout="wide")

    # Call the sidebar function to display sidebar content
    sidebar()

    # Navigation dropdown at the top
    selected_page = st.selectbox('Select Dashboard:', list(PAGES.keys()))

    # Run the app function for the selected page
    page = PAGES[selected_page]
    page()

if __name__ == "__main__":
    main()
