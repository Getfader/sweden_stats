from pyscbwrapper import SCB
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def get_energy_data():
    """
    Retrieves and processes energy production data from Statistics Sweden (SCB).

    Returns:
        DataFrame: Energy production data pivoted by year.
    """
    # Initialize SCB client
    scb = SCB('sv')

    # Navigate to the desired dataset
    scb.go_down('EN')
    scb.go_down('EN0105')
    scb.go_down('EN0105A')
    scb.go_down('ElProdAr')

    # Set query parameters
    scb.set_query(
        produktionsslag=[
            'total tillförsel av el',  # 'Tot'
            'vattenkraft',            # 'Vattenkraft'
            'pumpkraft',              # 'Pumpkraft'
            'kärnkraft',              # 'Karnkraft'
            'konventionell värmekraft, fjärrvärme',  # 'Kraftvf'
            'konventionell värmekraft, industri',   # 'Kraftvi'
            'vindkraft',              # 'Vind'
            'solkraft',               # 'sol'
            'import'                  # 'Imp'
        ],
        tabellinnehåll=['Brutto'],
        år=[str(year) for year in range(1986, 2023)])

    # Retrieve data
    data = scb.get_data()['data']

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Split the 'key' column into separate columns
    df[['category', 'year']] = pd.DataFrame(df['key'].tolist(), index=df.index)

    # Drop the original 'key' column
    df.drop('key', axis=1, inplace=True)

    # Rename the 'values' column
    df.rename(columns={'values': 'value'}, inplace=True)

    # Replace '..' with 0
    df['value'] = df['value'].apply(lambda x: float(x[0]) if x[0] != '..' else 0)

    # Convert the column to float type
    df['value'] = df['value'].astype(float)
    df['year'] = df['year'].astype(int)
    # Create Pivot table
    pivot_df = df.pivot_table(index='year', columns='category', values='value')

    category_map = {
        'Tot': 'Sum of Supply (GWh)',
        'Vattenkraft': 'Hydro',
        'Pumpkraft': 'Pumped Storage',
        'Karnkraft': 'Nuclear',
        'Kraftvf': 'Main Activity Producer CHP',
        'Kraftvi': 'Autoproducer CHP',
        'Vind': 'Wind',
        'sol': 'Solar',
        'Imp': 'Import',
    }

    # Rename pivot_df columns based on the mapping
    pivot_df = pivot_df.rename(columns=category_map)
    
    # Calculate the mean of each column
    column_means = pivot_df.mean()

    # Sort the columns based on their mean values in descending order
    sorted_columns = column_means.sort_values(ascending=False).index

    # Reorder the DataFrame columns based on the sorted column order
    pivot_df = pivot_df[sorted_columns]

    return pivot_df

def get_age_data():
    """
    Retrieves and processes population age data from Statistics Sweden (SCB).

    Returns:
        DataFrame: Population age data pivoted by year and gender.
    """

    # Initialize SCB client
    scb = SCB('sv')

    # Navigate to the desired dataset
    scb.go_down('BE')
    scb.go_down('BE0101')
    scb.go_down('BE0101B')
    scb.go_down('BefolkMedianAlder')

    # Set query parameters
    scb.set_query(kön=['män','kvinnor','totalt'],
                  tabellinnehåll=['Medelålder', 'Medianålder'], 
                  år=[str(year) for year in range(1968, 2024)])

    # Retrieve data
    data = scb.get_data()['data']

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Split the 'key' column into separate columns
    df[['category', 'year']] = pd.DataFrame(df['key'].tolist(), index=df.index)

    # Drop the original 'key' column
    df.drop('key', axis=1, inplace=True)

    # Extract mean age and median age from the 'values' column
    df['mean_age'] = df['values'].apply(lambda x: float(x[0]) if x[0] != '..' else np.nan)
    df['median_age'] = df['values'].apply(lambda x: float(x[1]) if x[1] != '..' else np.nan)

    # Drop the original 'values' column
    df.drop('values', axis=1, inplace=True)
    df['year'] = df['year'].astype(int)
    # Rename categories
    category_mapping = {'1': 'Male', '1+2': 'Overall', '2': 'Female'}
    df['category'] = df['category'].map(category_mapping)

    # Create Pivot table
    pivot_df = df.pivot_table(index='year', columns='category')

    return pivot_df

def get_healthcare_data():
    """
    Retrieves and processes healthcare spending data from Statistics Sweden (SCB).

    Returns:
        DataFrame: Healthcare spending data indexed by year.
    """
    # Initialize SCB client
    scb = SCB('sv')

    # Navigate to the desired dataset
    scb.go_down('NR')
    scb.go_down('NR0109')
    scb.go_down('HCBNP')

    # Set query parameters
    scb.set_query(tabellinnehål=['Totala hälso- och sjukvårdsutgifter, mnkr',
                                  'BNP till marknadspris, mnkr',
                                  'BNP relationstal, procent'],
                  år=[str(year) for year in range(2001, 2023)])

    # Retrieve data
    data = scb.get_data()['data']

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Split the 'key' column into separate columns
    df['year'] = pd.DataFrame(df['key'].tolist(), index=df.index).astype(int)

    # Drop the original 'key' column
    df.drop('key', axis=1, inplace=True)

    # Extract mean age and median age from the 'values' column
    df['Total healthcare costs'] = df['values'].apply(lambda x: float(x[0]) if x[0] != '..' else 0)
    df['GDP at marketprice'] = df['values'].apply(lambda x: float(x[1]) if x[1] != '..' else 0)
    df['GDP Percent %'] = df['values'].apply(lambda x: float(x[2]) if x[2] != '..' else 0)

    # Drop the original 'values' column
    df.drop('values', axis=1, inplace=True)

    df.set_index('year', inplace=True)

    return df

def get_construction_data():
    """
    Retrieves and processes construction cost data from Statistics Sweden (SCB).

    Returns:
        DataFrame: Construction cost data indexed by year and region.
    """
    # Initialize SCB client
    scb = SCB('sv')

    # Navigate to the desired dataset
    scb.go_down('BO')
    scb.go_down('BO0201')
    scb.go_down('BO0201A')
    scb.go_down('PrisPerAreorFH02')

    # Set query parameters
    scb.set_query(region=['Riket',
                          'Storstadsområdena',
                          'Stor-Stockholm',
                          'Stor-Göteborg',
                          'Stor-Malmö',
                          'Länsregionerna I - III',
                          'Länsregion I (norr)',
                          'Länsregion II (mitten)',
                          'Länsregion III (syd)'],
                  bruttonettopris='brutto',
                  tabellinnehål=['Byggnadsobjekt, antal som prisstatistiken baseras på',
                                'Lägenheter, antal som prisstatistiken baseras på',
                                'Lägenhetsarea/lägenhet, kvm',
                                'Markpris/lägenhetsarea, kr',
                                'Byggnadspris/lägenhetsarea, kr',
                                'Totalt produktionspris/lägenhetsarea, kr'],
                  år=[str(year) for year in range(1998, 2023)])

    # Retrieve data
    data = scb.get_data()['data']

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Split the 'key' column into separate columns
    df[['region','category','year']] = pd.DataFrame(df['key'].tolist(), index=df.index)
    df['year'] = df['year'].astype(int)

    region_mapping = {
        '00': 'The Country',
        '0001': 'Metropolitan Areas',
        '0010': 'Greater Stockholm',
        '0020': 'Greater Gothenburg',
        '0030': 'Greater Malmö',
        '0002': 'County Regions I - III',
        '4': 'County Region I (north)',
        '5': 'County Region II (central)',
        '6': 'County Region III (south)'
    }

    df['region'] = df['region'].replace(region_mapping)

    # Drop the original 'key' column
    df.drop('key', axis=1, inplace=True)

    # Extract mean age and median age from the 'values' column
    df['Amount of buildings'] = df['values'].apply(lambda x: float(x[0]) if x[0] != '..' else 0)
    df['Amount of apartments'] = df['values'].apply(lambda x: float(x[1]) if x[1] != '..' else 0)
    df['Apartment Area sqm/ Apartment'] = df['values'].apply(lambda x: float(x[2]) if x[2] != '..' else 0)
    df['Property cost/Apartment Area sqm'] = df['values'].apply(lambda x: float(x[3]) if x[3] != '..' else 0)
    df['Building cost/Apartment Area sqm'] = df['values'].apply(lambda x: float(x[4]) if x[4] != '..' else 0)
    df['Total Production costs / Apartment Area sqm'] = df['values'].apply(lambda x: float(x[5]) if x[5] != '..' else 0)

    # Drop the original 'values' column
    df.drop('values', axis=1, inplace=True)

    df.set_index('year', inplace=True)

    return df

def create_mean_median_chart(age_data, start_year, end_year):
    """
    Creates a line chart displaying the mean and median age over time.

    Args:
        age_data (DataFrame): Population age data.
        start_year (int): Start year for the chart.
        end_year (int): End year for the chart.

    Returns:
        plotly.graph_objects.Figure: Line chart displaying mean and median age.
    """
    # Filter data based on the selected time span
    filtered_data = age_data.loc[start_year:end_year]

    # Get Streamlit theme colors
    primary_color = st.get_option("theme.primaryColor")
    secondary_color = st.get_option("theme.secondaryBackgroundColor")

    fig = go.Figure()

    # Add mean age data
    fig.add_trace(go.Scatter(
        x=filtered_data.index, y=filtered_data['mean_age']['Overall'],
        mode='lines', name='Mean Age',
        line=dict(color=primary_color)))

    # Add median age data
    fig.add_trace(go.Scatter(
        x=filtered_data.index, y=filtered_data['median_age']['Overall'],
        mode='lines', name='Median Age',
        line=dict(color=secondary_color)))

    fig.update_layout(
        title='Mean and Median Age Over Time',
        xaxis_title='Year',
        yaxis_title='Age',
        legend=dict(y=0.9, x=1),
        xaxis=dict(range=[start_year, end_year]),
        yaxis=dict(showgrid=False),
        template='plotly_white'
    )

    return fig

def create_gender_age_chart(age_data, start_year, end_year):
    """
    Creates a line chart displaying mean and median age by gender over time.

    Args:
        age_data (DataFrame): Population age data.
        start_year (int): Start year for the chart.
        end_year (int): End year for the chart.

    Returns:
        plotly.graph_objects.Figure: Line chart displaying mean and median age by gender.
    """
    # Filter data based on the selected time span
    filtered_data = age_data.loc[start_year:end_year]

    # Colors for male and female
    male_color = '#2578BE'
    female_color = '#BE25B3'

    fig = go.Figure()

    # Add mean age data for males
    fig.add_trace(go.Scatter(
        x=filtered_data.index, y=filtered_data['mean_age']['Male'],
        mode='lines', name='Mean Age (Male)',
        line=dict(color=male_color)))

    # Add median age data for males
    fig.add_trace(go.Scatter(
        x=filtered_data.index, y=filtered_data['median_age']['Male'],
        mode='lines', name='Median Age (Male)',
        line=dict(color=male_color, dash='dash')))

    # Add mean age data for females
    fig.add_trace(go.Scatter(
        x=filtered_data.index, y=filtered_data['mean_age']['Female'],
        mode='lines', name='Mean Age (Female)',
        line=dict(color=female_color)))

    # Add median age data for females
    fig.add_trace(go.Scatter(
        x=filtered_data.index, y=filtered_data['median_age']['Female'],
        mode='lines', name='Median Age (Female)',
        line=dict(color=female_color, dash='dash')))

    fig.update_layout(
        title='Mean and Median Age Over Time by Gender',
        xaxis_title='Year',
        yaxis_title='Age',
        legend=dict(y=0.9, x=1),
        xaxis=dict(range=[start_year, end_year]),
        yaxis=dict(showgrid=False),
        template='plotly_white'
    )

    return fig

def create_stacked_bar_chart(selected_year_data, selected_years):
    """
    Creates a stacked bar chart displaying energy supply by source for a selected year range.

    Args:
        selected_year_data (DataFrame): Energy supply data for the selected year range.
        selected_years (tuple): Tuple containing the start and end years.

    Returns:
        plotly.graph_objects.Figure: Stacked bar chart displaying energy supply.
    """
    # Create a figure for the stacked bar chart
    fig = go.Figure()

    # Add traces for each energy source
    for column in selected_year_data.columns:
        if column != 'Sum of Supply (GWh)':  # Exclude 'Sum of Supply' column
            fig.add_trace(go.Bar(x=selected_year_data.index, y=selected_year_data[column], name=column))

    # Add annotations above each bar for 'Sum of Supply'
    for i, column in enumerate(selected_year_data.columns):
        if column == 'Sum of Supply (GWh)':
            for year, supply_value in zip(selected_year_data.index, selected_year_data[column]):
                fig.add_annotation(
                    x=year,  # X coordinate for the annotation
                    y=supply_value,  # Y coordinate for the annotation
                    text=f"{(supply_value/1000):.0f}K",  # Text of the annotation
                    showarrow=False,  # Show an arrow pointing to the bar
                    yshift=10
                )

    # Update layout
    fig.update_layout(
        barmode='stack',
        title=f'Energy Supply in Sweden ({selected_years[0]} - {selected_years[1]})',
        xaxis_title='Year',
        yaxis_title='GWh',
        template="plotly"
    )

    return fig

def calculate_average(data):
    """
    Calculates the average of a given dataset.

    Args:
        data (Series or DataFrame): Input data.

    Returns:
        float: Average value.
    """
    return data.mean()

def calculate_yearly_growth(data):
    """
    Calculates the yearly growth rate of a given dataset.

    Args:
        data (Series or DataFrame): Input data.

    Returns:
        Series or DataFrame: Yearly growth rates.
    """
    return data.pct_change() * 100  # Calculate percentage change

def calculate_metrics(filtered_data, selected_years, healthcare_data):
    """
    Calculates healthcare spending metrics.

    Args:
        filtered_data (DataFrame): Filtered healthcare spending data.
        selected_years (tuple): Tuple containing the start and end years.
        healthcare_data (DataFrame): Healthcare spending data.

    Returns:
        tuple: Tuple containing average spending, average yearly growth rate of healthcare spending,
               and average yearly growth rate of GDP.
    """
    # Calculate average healthcare spending
    average_spending = calculate_average(filtered_data['Total healthcare costs'])
    # Calculate yearly growth rate for healthcare spending
    yearly_growth_healthcare = calculate_yearly_growth(filtered_data['Total healthcare costs'])
    average_growth_healthcare = yearly_growth_healthcare.mean()
    # Filter GDP data for selected year range
    gdp_data_filtered = healthcare_data.loc[selected_years[0]:selected_years[1], 'GDP at marketprice']
    # Calculate yearly growth rate for GDP
    yearly_growth_gdp = calculate_yearly_growth(gdp_data_filtered)
    average_growth_gdp = yearly_growth_gdp.mean()

    return average_spending, average_growth_healthcare, average_growth_gdp

def format_difference(difference):
    """
    Formats a difference value into a human-readable string with a 'K' suffix.

    Args:
        difference (float): Difference value.

    Returns:
        str: Formatted difference string.
    """
    # Round to nearest thousand
    rounded_difference = round(difference / 1000, 1)

    # Convert to string with K suffix
    formatted_difference = f"{rounded_difference}K"

    return formatted_difference

def calculate_relative_percent_increase(data, region, start_year, end_year):
    """
    Calculates the relative percent increase in construction costs for a specific region over a specified time span.

    Args:
        data (DataFrame): Construction cost data indexed by year and region.
        region (str): Region for which the relative percent increase is calculated.
        start_year (int): Start year of the time span.
        end_year (int): End year of the time span.

    Returns:
        float: Relative percent increase in construction costs.
    """
    # Filter data for the selected region and year range
    region_data = data[(data["region"] == region) & (data.index >= start_year) & (data.index <= end_year)]

    # Extract the first and last values for the selected region
    first_value = region_data.iloc[0]['Total Production costs / Apartment Area sqm']
    last_value = region_data.iloc[-1]['Total Production costs / Apartment Area sqm']

    # Calculate the relative percent increase
    relative_percent_increase = ((last_value - first_value) / first_value) * 100

    return relative_percent_increase
