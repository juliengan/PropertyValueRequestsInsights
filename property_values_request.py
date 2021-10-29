#from matplotlib.colors import Normalize
import pandas as pd
import streamlit as st
#import pyarrow as pa
import numpy as np
import matplotlib.pyplot as plt
#import datetime as dt 
#from streamlit.elements.color_picker import ColorPickerMixin
import plotly_express as px
import seaborn as sns
#import time 
#import os
#import streamlit.components.v1 as components
#from bokeh.plotting import figure

@st.cache(allow_output_mutation=True)
def load_metadata(url):
    n = 100
    df = pd.read_csv(url, header=0, skiprows=lambda i: i % n != 0, parse_dates=['date_mutation'],dtype={("nature_mutation ","nom_commune","nature_culture"):"category",("valeur_fonciere","code_postal","surface_relle_bati","nombre_pieces_principales","surface_terrain","longitude","latitude") : "float32"})
    req_col=([ 'nature_mutation', 'adresse_numero', 'adresse_suffixe', 'adresse_nom_voie', 'adresse_code_voie', 'code_postal', 'code_commune', 
        'code_departement', 'ancien_code_commune', 'ancien_nom_commune', 'id_parcelle', 'ancien_id_parcelle', 
        'numero_volume', 'lot1_numero', 'lot1_surface_carrez', 'lot2_numero', 'lot2_surface_carrez', 'lot3_numero', 'lot3_surface_carrez', 
        'lot4_numero', 'lot4_surface_carrez', 'lot5_numero', 'lot5_surface_carrez', 'nombre_lots', 'code_type_local', 'type_local', 'surface_reelle_bati',
        'code_nature_culture', 'nature_culture', 'code_nature_culture_speciale', 'nature_culture_speciale', 'surface_terrain'])

    del req_col

    df['date_mutation'] = df['date_mutation'].astype(str)
    df['id_mutation'] = df['id_mutation'].astype(str)

    df.drop_duplicates(subset = "date_mutation")
    df.drop_duplicates(subset = "id_mutation")
    df.drop_duplicates(subset = "numero_disposition")
    df.drop_duplicates(subset = "valeur_fonciere")
    return df

def csv(app_mode):
    return str(app_mode)+ '_sample.csv'

def map(app_mode):
    st.header("Localisation of mutations in "+app_mode)
    data = pd.DataFrame({
    'awesome cities' : df['nom_commune'],
    'lat' : pd.to_numeric(df['latitude']),
    'lon' : pd.to_numeric(df['longitude'])
})
    cleaned = data.dropna()
    st.map(cleaned)

def pie_chart(df):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    st.header("Repartition of mutation type (sales, exchanges, expropriation, adjudication) "+app_mode)
    labels = 'Vente', 'Vente en l\'état futur d\'achèvement', 'Echange', 'Vente terrain à bâtir', 'Adjudication','Expropriation'
    sizes = df['nature_mutation'].value_counts(normalize=True) * 100
    explode = (0, 0, 0, 0,0,0)  
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, shadow=True, startangle=90,normalize=True,
    labeldistance = 1.3,autopct = lambda x: str(round(x, 2)) + '%',pctdistance = 0.7)
    #'''autopct='%1.1f%%',''',
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(bbox_to_anchor=(1,0), loc="lower right", labels=labels,bbox_transform=plt.gcf().transFigure)
    st.pyplot(fig1)


    '''plt.gca().axis("equal")
    pie = plt.pie(sizes, explode=explode, shadow=True, startangle=0,normalize=True,
    labeldistance = 1.3,autopct = lambda x: str(round(x, 2)) + '%',pctdistance = 0.7)
    plt.legend(pie[0],labels, bbox_to_anchor=(1,0.5), loc="center right", fontsize=10, 
            bbox_transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
'''
st.title("Project - Julie NGAN")
st.write("Data Visualization - Restitution des mutations à titres onéreux ")

st.sidebar.title("Année")
app_mode = st.sidebar.selectbox("",
        ["2016", "2017", "2018", "2019", "2020"])
#Data visualization : visual representation and analysis through different axes and aggregations
df = load_metadata(csv(app_mode))
st.write("Year "+app_mode)
map(app_mode)
pie_chart(df)
chart_data = df[['surface_reelle_bati','surface_terrain','valeur_fonciere']].copy()
st.line_chart(chart_data['valeur_fonciere'])
st.line_chart(chart_data[['surface_reelle_bati','surface_terrain']])

st.header("ID vs Date")
df['date_mutation'] = pd.to_datetime(df['date_mutation'])
fig2 = px.bar(df, x='date_mutation', y='id_mutation')
ts_chart = st.plotly_chart(fig2)

st.header("Valeur foncière vs Disposition number")
df['numero_disposition'] = pd.to_datetime(df['numero_disposition'])
fig3 = px.bar(df, x='numero_disposition', y='valeur_fonciere')
ts_chart = st.plotly_chart(fig3)

st.header("Histogram")
hist_values = np.histogram(df['date_mutation'].dt.hour, bins=24, range=(0,24))[0]




# Insights extraction to support analytical findings and decision making