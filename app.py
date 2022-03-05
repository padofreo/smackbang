import streamlit as st
import datetime
import time
import pandas as pd
import pydeck as pdk
import requests
from requests.structures import CaseInsensitiveDict

airports = pd.read_csv('data/airport_codes.csv')
matches_df = pd.DataFrame()

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

row1_1, row1_2 = st.columns((0.4, 1))

row1_1.image('images/smackbang_logo_v1.png', use_column_width='auto')
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

    # Get Origin One and Origin Two names for functions below
    city_one = airports.loc[airports['city_airport'] == origin_one_input, 'city' ].to_string(index=False)
    city_two = airports.loc[airports['city_airport'] == origin_two_input, 'city' ].to_string(index=False)

with row2_2:
    # Departure and return placeholder dates
    default_departure_date = datetime.date.today() + datetime.timedelta(days=14)
    future_date = default_departure_date + datetime.timedelta(days=50)

    # Departure and return date input fields
    departure_date = (st.date_input('Meeting Date', default_departure_date, min_value=datetime.date.today())).strftime("%d/%m/%Y")
    return_date_check = st.checkbox("Do you want to add a return date?")

    if return_date_check:
        return_date = (st.date_input('Return Date', future_date)).strftime("%d/%m/%Y")

    # Continent selection
    continent_input = st.selectbox('Continents', ('Asia', 'Africa', 'Europe', 'North America', 'South America', 'Oceania'))

    def continent_name(continent_input):
        result = {
                'Asia' : 'AS',
                'Africa' : 'AF',
                'Europe' : 'EU',
                'North America' : 'NA',
                'South America' : 'SA',
                'Oceania' : 'OC',
                }

        return result.get(continent_input)

    continent = continent_name(continent_input)



# ---------------------------
#        API Magic Area
# ---------------------------

    if st.button('SmackBang my Destinations'):
        # Spinner
        with st.spinner('Hold on while we search 1,000\'s of flights ...'):
            time.sleep(10)

        # Matches API query and output
        url = "https://smackbang-image-w76hg6ifha-ew.a.run.app/matches"

        headers = CaseInsensitiveDict()
        headers["accept"] = "application/json"

        query_string = {'origin_one':origin_one, 'origin_two':origin_two, 'departure_date':departure_date,
                        'continent':continent, 'return_date':'', 'currency':'USD'}

        result_matches = requests.get(url, headers=headers, params=query_string).json()
        matches_df = pd.DataFrame(result_matches)

        # Twitter API query
        url_twitter = "https://smackbang-image-w76hg6ifha-ew.a.run.app/twitter"

        matches_cities = matches_df.index.values

        keywords = ','.join(map(str,matches_cities))
        query_string_twitter = {'keywords':keywords}

        result = requests.get(url_twitter, headers=headers, params=query_string_twitter).json()       # --> my issue is here
        twitter_df = pd.DataFrame(result)
        twitter_df['City'] = twitter_df['City'].str.title()
        twitter_df = twitter_df.set_index('City')

# ---------------------------
#        User Output Header
# ---------------------------

row3_1, row3_2 = st.columns((1,1))

with row3_1:
    st.header('So what Destinations are looking good ...')

    if origin_one_input == 'Origin' or origin_two_input == 'Origin':
        st.markdown(f'Enter your destinations, dates and continent above.')
    else:
        st.markdown(f'Destinations between {city_one} and {city_two} are displayed below')

with row3_2:
    st.write('''  ''')
    st.write("I'm going to add the legends for the Fair Predictor and Verdict here")


row4_1, row4_2 = st.columns(2)

with row4_1:

# ------------------------------------------------
#        User output table creation and formatting
# ------------------------------------------------
    if origin_one_input == 'Origin' or origin_two_input == 'Origin' or matches_df.empty:
        st.write('')

    else:

        # Copy Matches API dataframe for user output and get only required series
        output_df = matches_df.copy()
        output_df = output_df.iloc[:,[0,1,14,12,13]]
        output_df = pd.merge(output_df, twitter_df, left_index=True, right_index=True)

        # Currency foramt for columns that need it
        pd.set_option('display.max_colwidth', None)
        output_df.iloc[:,0] = output_df.iloc[:,0].apply(lambda x: f"${x:,.0f}")
        output_df.iloc[:,1] = output_df.iloc[:,1].apply(lambda x: f"${x:,.0f}")
        output_df.iloc[:,2] = output_df.iloc[:,2].apply(lambda x: f"${x:,.0f}")

        # Add two columns for links to booking site
        output_df['Bookings'] = f'from {city_one}' + '#' + output_df.iloc[:,3]
        output_df['Bookings '] = f'from {city_two}' + '#' + output_df.iloc[:,4]   # Space after bookings_ is okay

        def make_clickable(val):
            name, url = val.split('#')
            return f'<a href="{url}">{name}</a>'

        # link is the column with hyperlinks
        output_df['Bookings'] = output_df['Bookings'].apply(make_clickable)
        output_df['Bookings '] = output_df['Bookings '].apply(make_clickable) # Space after bookings_ is okay

        # Final output as a HTML table so links work
        output_df = output_df.iloc[:,[0,1,2,5,6,7]]
        output_df = output_df.to_html(escape=False)
        st.write(output_df, unsafe_allow_html=True)


with row4_2:


# ---------------------------
#        Arc Layer
# ---------------------------
    if origin_one_input == 'Origin' or origin_two_input == 'Origin' or matches_df.empty:
        st.write('')

    else:

        # Get the data from the API query
        matches_map_query = matches_df.copy()

        # Get the index names (i.e. destination cities)
        map_np = matches_map_query.index.values

        # Origin One and Origin Two latitude and longitude coordinates
        origin_one_lat = airports.loc[airports['iata_code'] == origin_one, 'lat' ].to_string(index=False)
        origin_one_lon = airports.loc[airports['iata_code'] == origin_one, 'lon' ].to_string(index=False)
        origin_two_lat = airports.loc[airports['iata_code'] == origin_two, 'lat' ].to_string(index=False)
        origin_two_lon = airports.loc[airports['iata_code'] == origin_two, 'lon' ].to_string(index=False)


        # Origin One dataframe creation and population
        map_df = pd.DataFrame(map_np, columns=['dest_city'])
        map_df['origin_one'] = origin_one
        map_df['lat_origin_one'] = origin_one_lat
        map_df['lon_origin_one'] = origin_one_lon

        map_df = pd.merge(map_df, matches_map_query.iloc[:,16], how='inner', left_on='dest_city', right_index=True)
        map_df = pd.merge(map_df, matches_map_query.iloc[:,17], how='inner', left_on='dest_city', right_index=True)

        # Origin Two dataframe creation and population
        map_df2 = pd.DataFrame(map_np, columns=['dest_city'])
        map_df2['origin_one'] = origin_one
        map_df2['lat_origin_one'] = origin_one_lat
        map_df2['lon_origin_one'] = origin_one_lon

        map_df2 = pd.merge(map_df2, matches_map_query.iloc[:,16], how='inner', left_on='dest_city', right_index=True)
        map_df2 = pd.merge(map_df2, matches_map_query.iloc[:,17], how='inner', left_on='dest_city', right_index=True)

        # Start and end colours
        ORIGIN = [255, 0, 128]
        DESTINATION = [0, 200, 255]

        # The deck.gl ArcLayer
        st.pydeck_chart(pdk.Deck(
            map_provider='mapbox',
            map_style='mapbox://styles/mapbox/light-v10',

            initial_view_state = pdk.ViewState(
                latitude=0,
                longitude=80,
                bearing=0,
                pitch=45,
                zoom=0,
            ),

            layers=[
                pdk.Layer(
                    "ArcLayer",
                    data=map_df,
                    get_width=10,
                    get_source_position=[origin_one_lon, origin_one_lat],
                    get_target_position=["lon_", "lat_"],
                    get_tilt=10,
                    get_source_color=ORIGIN,
                    get_target_color=DESTINATION,
                    pickable=True,
                    auto_highlight=True,
                ),

                pdk.Layer(
                    "ArcLayer",
                    data=map_df2,
                    get_width=5,
                    get_source_position=[origin_two_lon, origin_two_lat],
                    get_target_position=["lon_", "lat_"],
                    get_tilt=10,
                    get_source_color=ORIGIN,
                    get_target_color=DESTINATION,
                    pickable=True,
                    auto_highlight=True,
                ),
            ],
        ))
