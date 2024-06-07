import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.helpers import get_energy_data, create_stacked_bar_chart

def app():
    """
    Main function to run the Streamlit application for visualizing energy production data in Sweden.

    This function displays interactive charts and summary statistics based on the selected year range.
    It calculates the average yearly growth rate and the top 5 sources with the highest yearly decrease in energy production.

    Returns:
        None
    """
    # Title and navigation
    st.title("Where does the Energy that Sweden consume come from?")

    # Load energy production data
    energy_data = get_energy_data()

    # Year range slider
    min_year = energy_data.index.min()
    max_year = energy_data.index.max()
    
    # Calculate the default range for the slider (10 latest years)
    default_min_year = max_year - 9 if max_year >= min_year + 9 else min_year
    default_max_year = max_year

    # Slider for selecting the year range
    selected_years = st.slider("Select Year Range", min_year, max_year, (default_min_year, default_max_year), step=1)

    # Filter data for the selected year range
    selected_year_data = energy_data.loc[selected_years[0]:selected_years[1]]

    # Calculate average yearly growth for each energy source
    yearly_growth = selected_year_data.pct_change().mean() * 100

    # Drop 'Sum of Supply (GWh)' as it's not an individual energy source
    yearly_growth = yearly_growth.drop('Sum of Supply (GWh)')

    # Filter out infinite growth rates
    yearly_growth = yearly_growth.replace([np.inf, -np.inf], np.nan).dropna()

    # Sort and get top 3 fastest-growing sources
    top_3_fastest_growing = yearly_growth.sort_values(ascending=False).head(5)
    top_3_fastest_growing_with_numbers = "\n".join([f"{i + 1}. {source}: {growth:.2f}%" for i, (source, growth) in enumerate(top_3_fastest_growing.items())])


    # Calculate yearly percentage decrease for each energy source
    yearly_decrease = (selected_year_data.iloc[-1] - selected_year_data.iloc[0]) / selected_year_data.iloc[0] * 100

    # Drop 'Sum of Supply (GWh)' as it's not an individual energy source
    yearly_decrease = yearly_decrease.drop('Sum of Supply (GWh)')

    # Filter out infinite and NaN values
    yearly_decrease = yearly_decrease.replace([np.inf, -np.inf], np.nan).dropna()

    # Sort and get top 3 sources with highest yearly decrease
    top_3_yearly_decrease = yearly_decrease.sort_values().head(5)
    top_3_yearly_decrease_with_numbers = "\n".join([f"{i + 1}. {source}: {decrease:.2f}%" for i, (source, decrease) in enumerate(top_3_yearly_decrease.items())])

    # Columns
    col1, col2 = st.columns([3, 7])  # 3/10 and 7/10 widths

    with col1:
        st.subheader(f"Energy Changes ({selected_years[0]}-{selected_years[1]})")
        # Display the list of top 3 fastest-growing sources
        st.markdown("##### **Top 5 Fastest Growing Sources (Average Yearly Growth Rate):**")
        st.markdown(top_3_fastest_growing_with_numbers)

        # Display the list of top 3 sources with highest yearly decrease
        st.markdown("##### **Top 5 Yearly Decrease in Energy Production:**")
        st.markdown(top_3_yearly_decrease_with_numbers)

    with col2:
        fig = create_stacked_bar_chart(selected_year_data, selected_years)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()
