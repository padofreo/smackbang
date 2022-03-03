import streamlit as st
import datetime
import base64
import pandas as pd
from streamlit_folium import folium_static
import folium
import requests
import os
from dotenv import load_dotenv, find_dotenv


env_path = find_dotenv()
load_dotenv(env_path)
RAPID_API_TOKEN = os.getenv('API_TOKEN')
RAPID_API_KEY = os.getenv('API_KEY')
airports = pd.read_csv('data/airport_codes.csv')
back_front_df = pd.DataFrame()

# ---------------------------
#        Page Configuration
# ---------------------------

st.set_page_config(
    page_title= 'SmackBang: Find the middle ground',
    page_icon= 'images/smackbang_favicon_32x32.png',
    layout= 'wide')

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

    # User One input, search and convert to string
    origin_one_input = st.selectbox('Origin 1', airports)
    origin_one = airports.loc[airports['city_airport'] == origin_one_input, 'iata_code' ].to_string(index=False)

    # User Two input, search and convert to string
    origin_two_input = st.selectbox('Origin 2', airports)
    origin_two = airports.loc[airports['city_airport'] == origin_two_input, 'iata_code' ].to_string(index=False)


with row2_2:
    # Departure and return placeholder dates
    default_departure_date = datetime.date.today()  + datetime.timedelta(days=28)
    future_date = default_departure_date + datetime.timedelta(days=10)

    # Departure and return date input fields
    departure_date = st.date_input('Meeting Date', default_departure_date)
    return_date = st.date_input('Return Date', future_date)

# ---------------------------
#        API Magic Area
# ---------------------------

    if st.button('Search'):
        city_url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/en-GB/cities.json"
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
                'x-access-token': "ccf49e56bc37cdcbea0545a0a08b7e08",
                'x-rapidapi-host': "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
                'x-rapidapi-key': "062d5d04d0msh9bf753a499a46f8p1d18edjsn469f78c5d3ac"
                    }

            response = requests.request("GET", url, headers=headers, params=querystring)

            return unpack(response.json())

        def query_origin_two(origin_two, page=100, currency="USD", departure_date= "", destination = "-"):

            querystring = {"origin": origin_two, "page":page, "currency":currency , "depart_date":departure_date, "destination": destination}

            headers = {
                'x-access-token': "ccf49e56bc37cdcbea0545a0a08b7e08",
                'x-rapidapi-host': "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
                'x-rapidapi-key': "062d5d04d0msh9bf753a499a46f8p1d18edjsn469f78c5d3ac"
                      }

            response = requests.request("GET", url, headers=headers, params=querystring)

            return unpack(response.json())

        def get_city_location(cities):
            headers = {
                'x-access-token': "ccf49e56bc37cdcbea0545a0a08b7e08",
                'x-rapidapi-host': "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
                'x-rapidapi-key': "062d5d04d0msh9bf753a499a46f8p1d18edjsn469f78c5d3ac"
            }

            response = requests.request("GET", city_url, headers=headers).json()

            city_location = []

            for city in cities:
                df = pd.DataFrame.from_dict(response)[['code', 'coordinates']].dropna()
                city_location.append(df.loc[df['code'] == city].coordinates.apply(pd.Series))
            result = pd.concat(city_location)
            df = pd.DataFrame(cities)

            result["city_code"] = df.values
            result.reset_index(inplace = True)
            result.drop(columns="index", inplace =True)
            return result

        def merge(query_origin_one,query_origin_two):
            df= query_origin_one.merge(query_origin_two, on= "city_code")[["city_code","price_x","price_y"]]

            df["sum"] = (df["price_x"] + df["price_y"]).apply(lambda x: f"${x:,.0f}")
            df['price_x'] = df['price_x'].apply(lambda x: f"${x:,.0f}")
            df['price_y'] = df['price_y'].apply(lambda x: f"${x:,.0f}")

            lat_lon_df = get_city_location(df['city_code'].values)
            final = df.merge(lat_lon_df, on="city_code")

            return final

        q1 = query_origin_one(origin_one)
        q2 = query_origin_two(origin_two)
        back_front_df = merge(q1,q2)


# ---------------------------
#        User Output
# ---------------------------

st.write(''' ''')

st.header('Destinations')
st.markdown('Destinations inbetween the two origins are displayed below')

row3_1, row3_2 = st.columns(2)

# Formatting Output dataframe

back_front_df.rename(columns = {'city_code':'Destination',
                                'price_x' : 'From Origin 1',
                                'price_y': 'From Origin 2',
                                'sum' : 'Combined Price',
                                }, inplace = True)

with row3_1:
    if not back_front_df.empty:
        st.dataframe(back_front_df[['Destination','From Origin 1','From Origin 2','Combined Price' ]].head(10).set_index('Destination'), 600, 400)
    else:
        st.write('')

with row3_2:

    df_map = back_front_df.iloc[:10]

    m = folium.Map(location=[0, 110], zoom_start=2, width='100%')

    for _, dest in df_map.iterrows():

        folium.Marker(
            location=[dest.lat, dest.lon],
            popup= [dest.Destination, dest['From Origin 1'],dest['From Origin 2'],dest['Combined Price'] ],
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    folium_static(m)

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
