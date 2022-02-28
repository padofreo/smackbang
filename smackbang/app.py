import streamlit as st
import datetime
import base64

# ---------------------------
#        Header
# ---------------------------

''' # Smackbang:  Find the middle ground '''

# ---------------------------
#        User Input
# ---------------------------

# User One Location
origin_one = st.text_input('Origin 1', placeholder = 'Country, city or airport')

# User Two Location
origin_two = st.text_input('Origin 2', placeholder = 'Country, city or airport')

# Departure Date
departure_date = st.date_input('Meeting Date', datetime.date(2022, 3, 1))

# Return Date
return_date = st.date_input('Return Date', datetime.date(2022, 3, 10))

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

image_path = 'images/smackbang_logo_v1.png'

st.write(background_image_style(image_path), unsafe_allow_html=True)
