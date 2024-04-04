# Property Values Resquests Insights

## Goal of the project
The goal of the project is to make data visualisation to help making insights decisions out of it.

The data we operate is public : property values requests /annual files of refunds of transfers for valuable consideration from France from 2016 to 2020.

It gives initially 40 variables : date mutation, id_mutation, numero_disposition, adresse, id_parcelle, type_local, nature_mutation, gps coordinates...


## 1. Data Loading
### Sampling disclaimer
I sampled the original csv files (at 1%) and create new ones from them : 10 485 row data. Indeed, the data was too heavy to be handled by github. 
Another solution would be to use bucket S3 provided by Amazon.

## 2. Explore and Process : Data cleaning, pre-processing, transformation and enrichment

I load the csv files in dataframes

I had first to preprocess the dataframes by dropping all empty columns as welle as drop missing information in some rows.

Thanks to pandas_profilling, I was able to see the high correlations variables have between each other and extract that visually with plots using streamlit 
in python.

I sort the date_mutation after converting it into datetime type and I set it a the index of the dataframe, especially useful to interpret the line charts (evolution of valeur fonciere, surface réelle bâtie and surface terrain) 

## 3. Data visualization : visual representation and analysis through different axes and aggregations
## 4. Insights extraction to support analytical findings and decision making


## How to use my application

You'll have to select one of the checkbox to see the data visualisation
