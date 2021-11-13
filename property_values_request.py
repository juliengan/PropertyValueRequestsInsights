from matplotlib.colors import Normalize
import pandas as pd
import streamlit as st
#import pyarrow as pa
import numpy as np
import matplotlib.pyplot as plt
#import datetime as dt 
#from streamlit.elements.color_picker import ColorPickerMixin
import plotly_express as px
import seaborn as sns
import time 
#import os
import streamlit.components.v1 as components
#from bokeh.plotting import figure
@st.cache(allow_output_mutation=True)
def get_dom(dt):
    return dt.day 


@st.cache(allow_output_mutation=True)
def get_weekday(dt):
    return dt.weekday()

@st.cache(suppress_st_warning=True, allow_output_mutation=True) 
def log(func):
    def wrapper(*args,**kwargs):
        with open("logs.txt","a") as f:
            before = time.time()
            func()
            f.write("Called function with " + str(time.time() - before) + " seconds " + "\n")
            #f.write("Called function with " + " ".join([str(arg) for arg in args]) + " at " + str(datetime.datetime.now()) + "\n")
        val = func(*args,**kwargs)
        return val
    return wrapper


@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def load_metadata(url):
    n = 100
    #, skiprows=lambda i: i % n != 0
    df = pd.read_csv(url, header=0, parse_dates=['date_mutation'],
    skipinitialspace = True,
    dtype={("nature_mutation ","nom_commune","nature_culture"):"category",("valeur_fonciere","code_postal","surface_relle_bati","nombre_pieces_principales","surface_terrain","longitude","latitude") : "float32"})
    df['date_mutation'] = pd.to_datetime(df['date_mutation'])
    #df['date_mutation'] = df['date_mutation'].astype(str)
    df['id_mutation'] = df['id_mutation'].astype(str)
    df = df.drop(columns= ['adresse_suffixe','adresse_numero','ancien_code_commune', 'ancien_nom_commune',
                           'ancien_id_parcelle', 
        'numero_volume', 'lot1_numero', 'lot1_surface_carrez', 'lot2_numero', 
                           'lot2_surface_carrez', 'lot3_numero', 'lot3_surface_carrez', 
        'lot4_numero', 'lot4_surface_carrez', 'lot5_numero', 'lot5_surface_carrez'])
    df['adresse_nom_voie'] = df['adresse_nom_voie'].dropna()
    df["nombre_pieces_principales"] = df["nombre_pieces_principales"].dropna()
    df['surface_reelle_bati'] = df['surface_reelle_bati'].dropna()
    df['type_local'] = df['type_local'].dropna()
    df['code_type_local'] = df['code_type_local'].dropna()
    df["longitude"] = df["longitude"].dropna()
    df["latitude"] = df["latitude"].dropna()
    df['surface_terrain'] = df['surface_terrain'].dropna()
    
    df['code_nature_culture'] = df['code_nature_culture'].dropna()
    df['nature_culture'] = df['nature_culture'].dropna()
    df['code_nature_culture_speciale'] = df['code_nature_culture_speciale'].dropna()
    df['nature_culture_speciale'] = df['nature_culture_speciale'].dropna()
    df['code_type_local'] = df['code_type_local'].dropna()
    df['type_local'] = df['type_local'].dropna()
    df['nature_mutation'] = df['nature_mutation'].dropna()



    df['dom'] = df['date_mutation'].map(get_dom)
    df['weekday'] = df['date_mutation'].map(get_weekday)
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
    st.header("Repartition of mutation type (sales, exchanges, expropriation, adjudication) "+app_mode)
    labels = 'Vente', 'Vente en l\'état futur d\'achèvement', 'Echange', 'Vente terrain à bâtir', 'Adjudication','Expropriation'
    sizes = df['nature_mutation'].value_counts(normalize=True) * 100
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, shadow=True, startangle= 100, autopct=lambda x: str(round(x, 2)),pctdistance = 0.7)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(bbox_to_anchor=(1,0), loc="lower right", labels=labels,bbox_transform=plt.gcf().transFigure)
    st.pyplot(fig1)

def type_local_repart(df):
    st.header("Repartition of local types "+ app_mode)
    labels = 'Maison','Appartement', 'Dépendance', 'Local industriel. commercial ou assimilé'
    sizes = df['type_local'].value_counts(normalize=True) * 100
    explode = (0.1,0,0,0)  
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, shadow=True, startangle=100,normalize=True,autopct=lambda x: str(round(x, 2)) + '%',labels=labels,explode=explode)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)


def histogram(rows):
    weekdays = st.expander("Weekdays available in our dataset")
    fig4, weekdaysax = plt.subplots()
    plt.title(rows.name)
    weekdaysax = plt.hist(rows, range = (-0.5, 6.5), bins = 7, rwidth = 0.8)
    plt.title("Frequency by " + rows.name)
    plt.xlabel(rows.name)
    plt.ylabel("Frequency")
    weekdays.pyplot(fig4)

def valeur_fonciere_vs_date():
    st.header("Land value fluctuation through time")
    df['date_mutation'] = pd.to_datetime(df['date_mutation'])
    fig3 = px.bar(df, x='date_mutation', y='valeur_fonciere')
    ts_chart = st.plotly_chart(fig3)


def valeur_fonciere_vs_department():
    st.header("Land value fluctuation by departments")
    fig3 = px.bar(df, x='code_departement', y='valeur_fonciere')
    ts_chart = st.plotly_chart(fig3)


def surface_terrain_vs_department():
    st.header("Land value fluctuation by departments")
    fig3 = px.bar(df, x='code_departement', y='surface_terrain')
    ts_chart = st.plotly_chart(fig3)


st.title("Project - Julie NGAN")
st.write("Data Visualization - Return of transfers against payment ")

st.sidebar.title("Year")
app_mode = st.sidebar.selectbox("",
        ["2016", "2017", "2018", "2019", "2020"])
#Data visualization : visual representation and analysis through different axes and aggregations
df = load_metadata(csv(app_mode))
st.write("Year "+app_mode)
#st.write(df)
map(app_mode)
pie_chart(df)
type_local_repart(df)

st.line_chart(df['valeur_fonciere'])
st.line_chart(df[['surface_reelle_bati','surface_terrain']])


valeur_fonciere_vs_date()
valeur_fonciere_vs_department()
surface_terrain_vs_department()

st.header("Histogram")
hist_values = np.histogram(df['date_mutation'].dt.hour, bins=24, range=(0,24))[0]

histogram(df['weekday'])
histogram(df['dom'])
components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div id="accordion">
            <div class="card">
                <div class="card-header" id="headingOne">
                <h5 class="mb-0">
                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                    Weekdays available in the dataset 📚
                    </button>
                </h5>
                </div>
                <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
                <div class="card-body">
                    <iframe src="https://informationisbeautiful.net/visualizations/words-shakespeare-invented/" title="Shakespeare's invented words" ,width=1024,height=768)
                </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header" id="headingTwo">
                <h5 class="mb-0">
                    <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                    Point Cloud
                    </button>
                </h5>
                </div>
                <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
                <div class="card-body">
                    <iframe src="https://informationisbeautiful.net/visualizations/words-shakespeare-invented/" title="Shakespeare's invented words" ,width=1024,height=768)
                </div>
                </div>
            </div>
        </div>
        """,
        height=600
    )

"""if __name__ == "__main__":
    main()"""












# Insights extraction to support analytical findings and decision making