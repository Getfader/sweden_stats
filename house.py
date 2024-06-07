import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.helpers import get_construction_data, format_difference, calculate_relative_percent_increase

def app():
    """
    Display a Streamlit app for visualizing construction data related to apartment costs in Sweden.

    This function sets up a Streamlit app to visualize construction data related to apartment costs in Sweden.
    It loads construction data, filters it based on the selected year range, and calculates various metrics.
    The app displays the difference between the cheapest and most expensive regions in terms of apartment costs,
    both in actual value and relative percentage.
    Additionally, it allows users to select a specific region and calculates the relative percent increase in apartment costs.
    It also plots a line chart comparing the square meter price between different regions over the selected years.

    Returns:
        None
    """
    st.title("How much does it cost to build new apartments in Sweden?")

    # Load construction data
    construction_data = get_construction_data()

    # Filter by year range
    min_year = int(construction_data.index.min())
    max_year = int(construction_data.index.max())
    selected_years = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))

    # Filter data based on selected year range
    filtered_data = construction_data[(construction_data.index >= selected_years[0]) &
                                      (construction_data.index <= selected_years[1])]

    # Columns
    col1, col2 = st.columns([3,7])

    if not filtered_data.empty:
        # Calculate difference between highest and lowest values for the latest year
        latest_year_data = filtered_data.loc[selected_years[1]]
        highest_value = latest_year_data['Total Production costs / Apartment Area sqm'].max()
        lowest_value = latest_year_data['Total Production costs / Apartment Area sqm'].min()
        difference_actual = highest_value - lowest_value
        difference_actual_formatted = format_difference(difference_actual)

        # Calculate relative percentage difference
        difference_percentage = ((highest_value - lowest_value) / lowest_value) * 100

        # Display big numbers using st.metric() in the left column
        with col1:
            # Format the subheader string
            subheader_text = "Difference between cheapest and most expensive region:"

            # Display the subheader
            st.subheader(subheader_text)

            # Display big numbers using st.metric() in the left column
            st.metric(label="Difference (Actual value)", value=difference_actual_formatted)
            st.metric(label="Difference (Relative percentage)", value=f"{difference_percentage:.2f}%")

            # Dropdown to select region for relative percent increase calculation
            selected_region = st.selectbox("Select Region for Relative Percent Increase", construction_data["region"].unique())

            if selected_region in construction_data["region"].unique():
                # Calculate relative percent increase using the new function
                relative_percent_increase = calculate_relative_percent_increase(construction_data, selected_region, selected_years[0], selected_years[1])

                st.subheader(f"Relative percent increase in {selected_region} from {selected_years[0]} to {selected_years[1]}:")
                st.metric(label="Relative Percent Increase", value=f"{relative_percent_increase:.2f}%")
            else:
                st.write(f"No data available for the region: {selected_region}")

        with col2:
            st.subheader("Comparing square meter price between different regions")

            # Create a line plot
            fig = go.Figure()

            # Add traces for each region
            for region, data in filtered_data.groupby('region'):
                fig.add_trace(go.Scatter(x=data.index, y=data['Total Production costs / Apartment Area sqm'],
                                         mode='lines',
                                         name=region))

            # Update layout to match Streamlit theme and remove gridlines
            fig.update_layout(
                title=f"Total Production Costs per Square Meter ({selected_years[0]} - {selected_years[1]})",
                xaxis_title="Year",
                yaxis_title="SEK",
                showlegend=True,
                plot_bgcolor=st.get_option("theme.backgroundColor"),
                paper_bgcolor=st.get_option("theme.secondaryBackgroundColor"),
                font_color=st.get_option("theme.textColor"),
                xaxis=dict(showgrid=False),  # Remove x-axis gridlines
                yaxis=dict(showgrid=False)   # Remove y-axis gridlines
            )

            # Plot the figure
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("No data available for the selected year range.")

if __name__ == "__main__":
    app()
