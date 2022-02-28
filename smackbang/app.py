import streamlit as st
import datetime
import base64
import pandas as pd
import numpy as np

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
        response = requests.get(url, params=fare_details).json()    # NEED TO ADD API DETAILS HERE
        #fare_pred = round(response.get("flight_prices"),2)


# ---------------------------
#        User Output
# ---------------------------

st.write(''' ''')

st.header('Destinations')
st.markdown('Destinations are displayed in ascending order of the combined price for all passenngers')


row3_1, row3_2 = st.columns((1,2))

with row3_1:
    df = pd.read_csv('smackbang/data/dummy_data.csv')               # Read the dummy data set
    st.write(df.head())                                             # Show dummy data set dataframe

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
