import streamlit as st
import plotly.graph_objects as go
from utils.helpers import get_healthcare_data, calculate_metrics, format_to_billions

def app():
    """
    Display a Streamlit app for visualizing healthcare spending data.

    This function sets up a Streamlit app to visualize healthcare spending data for Sweden.
    It loads healthcare data, filters it based on the selected year range, and calculates various metrics.
    The app displays metrics such as the proportion of healthcare spending to total GDP,
    average healthcare spending, average yearly growth rates for healthcare spending and GDP,
    and a stacked bar chart showing total healthcare costs and remaining GDP over the selected years.

    Returns:
        None
    """
    # Title and navigation
    st.title("How much money does Sweden spend on Healthcare?")

    # Load healthcare data
    healthcare_data = get_healthcare_data()

    # Filter data based on selected year range
    min_year = int(healthcare_data.index.min())
    max_year = int(healthcare_data.index.max())

    # Calculate the default range for the slider (10 latest years)
    default_min_year = max_year - 9 if max_year >= min_year + 9 else min_year
    default_max_year = max_year

    # Slider for selecting the year range
    selected_years = st.slider("Select Year Range", min_year, max_year, (default_min_year, default_max_year), step=1)

    filtered_data = healthcare_data.loc[selected_years[0]:selected_years[1]]

    # Calculate the remaining GDP after subtracting healthcare costs
    filtered_data['Remaining GDP'] = (filtered_data['GDP at marketprice'] - filtered_data['Total healthcare costs'])

    # Columns
    col1, col2 = st.columns([3, 7])  # 3/10 and 7/10 widths

    with col1:
        # Subheader providing context for the metrics
        st.subheader("Healthcare Metrics")

        # Display GDP percentage for the last selected year
        last_year = selected_years[1]
        gdp_percentage = healthcare_data.loc[last_year, 'GDP Percent %']

        # Calculate delta from the year before
        prev_year_gdp_percentage = healthcare_data.loc[last_year - 1, 'GDP Percent %']
        delta_gdp_percentage = gdp_percentage - prev_year_gdp_percentage

        # Show metric
        st.metric(label=f"Healthcare Proportion of Total GDP for {last_year} and change from previous year", value=f"{gdp_percentage:.2f}%", delta=f"{delta_gdp_percentage:.2f}%")

        # Calculate metrics
        average_spending, average_growth_healthcare, average_growth_gdp = calculate_metrics(filtered_data, selected_years, healthcare_data)

        # Show metrics
        st.metric(label=f"Average Healthcare Spending ({selected_years[0]} - {selected_years[1]})", value=format_to_billions(average_spending))
        st.metric(label=f"Average Yearly Growth Rate for Healthcare Spending ({selected_years[0]} - {selected_years[1]})", value=f"{average_growth_healthcare:.2f}%")
        st.metric(label=f"Average Yearly Growth Rate for GDP ({selected_years[0]} - {selected_years[1]})", value=f"{average_growth_gdp:.2f}%")

    with col2:
        # Create stacked bar chart
        fig = go.Figure()

        # Add total healthcare costs as the base bar
        fig.add_trace(go.Bar(x=filtered_data.index,
                            y=filtered_data['Total healthcare costs'],
                            name='Total Healthcare Costs',
                            marker_color=st.get_option("theme.secondaryBackgroundColor"),  # Match Streamlit theme
                            hovertemplate='%{y}'
                            ))

        # Add the remaining GDP as the stacked bar on top of healthcare costs
        fig.add_trace(go.Bar(x=filtered_data.index,
                            y=filtered_data['Remaining GDP'],
                            name='GDP excluding healthcare costs',  # Updated label
                            marker_color=st.get_option("theme.primaryColor"),  # Match Streamlit theme
                            hovertemplate='%{y}'
                            ))

            # Add annotations at the top of each bar
        for i, row in filtered_data.iterrows():
            # Use the function to format the value for annotation
            gdp_value_billions = format_to_billions(row['GDP at marketprice'])  # Or use another column for annotations
            
            # Adjust the y position to be slightly above the top of the bar
            fig.add_annotation(
                x=i,
                y=row['GDP at marketprice'] + (row['GDP at marketprice'] * 0.02),  # Add 2% of the value for spacing
                text=gdp_value_billions,
                showarrow=False,
                font=dict(size=12, color="#ffffff"),
                align="center",
                bgcolor="rgba(0,0,0,0.5)",
                xanchor="center",
                yanchor="bottom"
            )

        # Update layout to remove gridlines
        fig.update_layout(barmode='stack', title=f'Total Healthcare Costs vs. GDP at Market Price ({selected_years[0]} - {selected_years[1]})',
                        xaxis_title='Year', yaxis_title='Thousand SEK',
                        template="plotly", xaxis=dict(showgrid=False),     yaxis=dict(showgrid=False))

        # Show plot
        st.plotly_chart(fig)

if __name__ == "__main__":
    app()
