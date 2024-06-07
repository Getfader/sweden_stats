import streamlit as st
import plotly.graph_objects as go
from utils.helpers import get_age_data, create_mean_median_chart, create_gender_age_chart

def app():
    """
    Main function to run the Streamlit application for visualizing Swedish population age data.

    This function displays interactive charts and summary statistics based on the selected time span and chart type.
    """
    # Title
    st.title("How old is the Swedish population?")

    # Load age data
    age_data = get_age_data()

    # Slider for selecting time span
    start_year, end_year = st.slider("Select Time Span",
                                     min_value=1968, max_value=2023,
                                     value=(1968, 2023), step=1)

    # Columns
    col1, col2 = st.columns([3, 7])  # 3/10 and 7/10 widths
    with col1:
        subcol1, subcol2 = st.columns(2)
        with subcol2:
            # Radio button to toggle between chart types
            chart_type = st.radio("Select Chart Type",
                                  options=["Mean vs Median", "Male vs Female"])
        with subcol1:
            if chart_type == "Mean vs Median":
                st.markdown("#### Summary Statistics")
                # Mean and median age over the entire selected range
                mean_age_overall = age_data['mean_age']['Overall'].loc[start_year:end_year].mean()
                median_age_overall = age_data['median_age']['Overall'].loc[start_year:end_year].median()

                st.metric(f"Mean Age ({start_year}-{end_year})", f"{mean_age_overall:.2f}")
                st.metric(f"Median Age ({start_year}-{end_year})", f"{median_age_overall:.2f}")

                # Change in metrics over the selected time span
                mean_age_change = age_data['mean_age']['Overall'].loc[end_year] - age_data['mean_age']['Overall'].loc[start_year]
                median_age_change = age_data['median_age']['Overall'].loc[end_year] - age_data['median_age']['Overall'].loc[start_year]

                st.metric(f"Mean Age Change ({start_year}-{end_year})", f"{mean_age_change:.2f}")
                st.metric(f"Median Age Change ({start_year}-{end_year})", f"{median_age_change:.2f}")

            else:
                st.markdown("#### Summary Statistics")
                # Display other relevant metrics for male vs female chart
                st.metric(f"Male Mean Age ({start_year}-{end_year})", f"{age_data['mean_age']['Male'].loc[start_year:end_year].mean():.2f}")
                st.metric(f"Female Mean Age ({start_year}-{end_year})", f"{age_data['mean_age']['Female'].loc[start_year:end_year].mean():.2f}")
                st.metric(f"Male Median Age ({start_year}-{end_year})", f"{age_data['median_age']['Male'].loc[start_year:end_year].median():.2f}")
                st.metric(f"Female Median Age ({start_year}-{end_year})", f"{age_data['median_age']['Female'].loc[start_year:end_year].median():.2f}")

    with col2:
        # Show the chart based on selected type
        if chart_type == "Mean vs Median":
            fig = create_mean_median_chart(age_data, start_year, end_year)
        else:
            fig = create_gender_age_chart(age_data, start_year, end_year)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()
