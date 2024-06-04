from pyscbwrapper import SCB
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

def get_energy_data():
    # Initialize SCB client
    scb = SCB('sv')

    # Navigate to the desired dataset
    scb.go_down('EN')
    scb.go_down('EN0105')
    scb.go_down('EN0105A')
    scb.go_down('ElProdAr')

    # Set query parameters
    scb.set_query(produktionsslag=['total tillförsel av el',
                                   'vattenkraft',
                                   'pumpkraft',
                                   'kärnkraft',
                                   'konventionell värmekraft, fjärrvärme',
                                   'konventionell värmekraft, industri',
                                   'vindkraft',
                                   'solkraft',
                                   'konventionell värmekraft, kondensproduktion',
                                   'konventionell värmekraft, gasturbin- och annan produktion',
                                   'import'], 
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

    # Create Pivot table
    pivot_df = df.pivot_table(index='year', columns='category', values='value')

    # Rename columns
    pivot_df.columns=['Gas Turbines', 'Import', 'Nuclear', 'Condensing Turbines', 
                      'Main Activity Producer CHP', 'Autoproducer CHP', 'Pumped Storage', 
                      'Sum of Supply (GWh)', 'Hydro', 'Wind', 'Solar']

    return pivot_df

def get_age_data():
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

    # Rename categories
    category_mapping = {'1': 'Male', '1+2': 'Total', '2': 'Female'}
    df['category'] = df['category'].map(category_mapping)

    # Create Pivot table
    pivot_df = df.pivot_table(index='year', columns='category')

    return pivot_df

def get_healthcare_data():
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
    df['year'] = pd.DataFrame(df['key'].tolist(), index=df.index)

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




def create_plotly_figure_age(df):
    # Create a figure
    fig = go.Figure()

    # Add the first trace with blue color
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df[('mean_age', 'Male')], 
        mode='lines', 
        name='Mean Male Age',
        line=dict(width=2, color='blue')
    ))

    # Add the second trace with red color
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df[('mean_age', 'Female')], 
        mode='lines', 
        name='Mean Female Age',
        line=dict(width=2, color='red')
    ))

    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df[('mean_age', 'Total')], 
        mode='lines', 
        name='Mean Overall Age',
        line=dict(width=2, color='green')
    ))

    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df[('median_age', 'Male')], 
        mode='lines', 
        name='Median Male Age',
        line=dict(dash='dash', width=2, color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df[('median_age', 'Female')], 
        mode='lines', 
        name='Median Female Age',
        line=dict(dash='dash', width=2, color='red')
    ))

    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df[('median_age', 'Total')], 
        mode='lines', 
        name='Median Overall Age',
        line=dict(dash='dash',width=2, color='green')
    ))

    # Customizations
    fig.update_layout(
        title='Age over the years',
        xaxis_title='Time',
        yaxis_title='Age',
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    return fig





fig = create_plotly_figure_age(get_age_data())
# Streamlit app
st.title("Sweden")
with st.container():
   st.write("Exploring age in Sweden")
   st.plotly_chart(fig, theme='streamlit')



# Display the plot
