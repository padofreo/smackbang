import streamlit as st
import datetime
import base64
import pandas as pd
import numpy as np
import requests
import os

API_KEY = os.environ['API_KEY']
# ---------------------------
#        Page Configuration
# ---------------------------

st.set_page_config(
    page_title= 'SmackBang: Find the middle ground',
    page_icon= 'images/smackbang_favicon_32x32.png',
    layout= 'wide') # 'centered' 'wide'

# Remove the menu button from Streamlit
st.markdown(""" <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style> """, unsafe_allow_html=True)


# ---------------------------
#        Header
# ---------------------------

row1_1, row1_2 = st.columns((0.2, 2))

row1_1.image('images/smackbang_favicon_32x32.png', width = 120)
row1_2.title('SmackBang:  Find the middle ground')
row1_2.markdown('Connect with friends, family and colleagues')


# ---------------------------
#        User Input
# ---------------------------

row2_1, row2_2 = st.columns((1,1))

with row2_1:
    origin_one = st.text_input('Origin 1', placeholder = 'Country, city or airport') # User One Location
    origin_two = st.text_input('Origin 2', placeholder = 'Country, city or airport') # User Two Location

with row2_2:
    todays_date = datetime.date.today()                             # Default departure date is today.  can't travel back in time
    future_date = todays_date + datetime.timedelta(days=10)         # Default return dat is 10 days.
    departure_date = st.date_input('Meeting Date', todays_date)     # Departure Date
    return_date = st.date_input('Return Date', future_date)         # Return Date

# ---------------------------
#        API Magic Area
# ---------------------------

    if st.button('Search'):
        #response = requests.get(url, params=fare_details).json()    # NEED TO ADD API DETAILS HERE
        #fare_pred = round(response.get("flight_prices"),2)

        url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v1/prices/cheap"

        def unpack(d):

            df = {'city_code':[], 'price':[], 'airline':[], 'flight_number':[],
            'departure_at':[], 'return_at':[], 'expires_at':[]}

            for key1, value in d['data'].items():

                for key, value2 in value.items():
                    df['city_code'].append(key1)
                    for key, value3 in value2.items():
                        df[key].append(value3)

            return pd.DataFrame(df)

        def query_origin_one(origin_one, page=100, currency="USD", departure_date= "", destination = "-"):

            querystring = {"origin": origin_one, "page":page, "currency":currency , "depart_date": departure_date, "destination": destination}

            headers = {
                'x-access-token': API_KEY,
                'x-rapidapi-host': "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
                'x-rapidapi-key': "062d5d04d0msh9bf753a499a46f8p1d18edjsn469f78c5d3ac"
                    }

            response = requests.request("GET", url, headers=headers, params=querystring)

            return unpack(response.json())

        def query_origin_two(origin_two, page=100, currency="USD", departure_date= "", destination = "-"):

            querystring = {"origin": origin_two, "page":page, "currency":currency , "depart_date":departure_date, "destination": destination}

            headers = {
                'x-access-token': API_KEY,
                'x-rapidapi-host': "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
                'x-rapidapi-key': "062d5d04d0msh9bf753a499a46f8p1d18edjsn469f78c5d3ac"
                      }

            response = requests.request("GET", url, headers=headers, params=querystring)

            return unpack(response.json())

        def merge(query_origin_one,query_origin_two):
            df= query_origin_one.merge(query_origin_two, on= "city_code")[["city_code","price_x","price_y"]]
            df["sum"] = df["price_x"] + df["price_y"]
            return df

        q1 = query_origin_one(origin_one)
        q2 = query_origin_two(origin_two)
        back_front_df = merge(q1,q2)

# ---------------------------
#        User Output
# ---------------------------

st.write(''' ''')

st.header('Destinations')
st.markdown('Destinations are displayed in ascending order of the combined price for all passenngers')


row3_1, row3_2 = st.columns((1,2))

with row3_1:
    #df = pd.read_csv('smackbang/data/dummy_data.csv')               # Read the dummy data set
    st.write(back_front_df)                                             # Show dummy data set dataframe

with row3_2:
    st.map(data=None, zoom=None, use_container_width=True)          # Map for results


# ---------------------------
#     Background Image
# ---------------------------


@st.cache
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:image/png;base64,{encoded}">'
    return tag

def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style

image_path = 'images/smackbang_world_map.png'

#st.write(background_image_style(image_path), unsafe_allow_html=True)

def unpack(d):

    df = {'city_code':[], 'price':[], 'airline':[], 'flight_number':[],
         'departure_at':[], 'return_at':[], 'expires_at':[]}

    for key1, value in d['data'].items():

        for key, value2 in value.items():
            df['city_code'].append(key1)

            for key, value3 in value2.items():

                df[key].append(value3)

    #return df
    return pd.DataFrame(df)
