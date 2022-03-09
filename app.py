import streamlit as st
import datetime
import time
import pandas as pd
import numpy as np
import pydeck as pdk
import requests
from requests.structures import CaseInsensitiveDict
import multipart
from smackbang.predict_prepro import process_matches

airports = pd.read_csv('data/airport_codes.csv')
matches_df = pd.DataFrame()
preds_df1 = pd.DataFrame()
preds_df2 = pd.DataFrame()

# ---------------------------
#        Page Configuration
# ---------------------------

st.set_page_config(
    page_title= 'SmackBang: Find the middle ground',
    page_icon= 'images/smackbang_favicon_32x32.png',
    layout= 'wide')

# Remove the menu button and footer note from Streamlit
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True)



# ---------------------------
#        Header
# ---------------------------

row1_1, row1_2 = st.columns((0.4, 1))

row1_1.image('images/smackbang_logo_v1.png', use_column_width='auto')
row1_2.title('SmackBang:  Find the middle ground')
row1_2.write(
"""Connect with friends, family and colleagues with our easy to use tool. Batch 796 has done all the hard work for you.

Enter details in the fields below and we'll get cracking finding great destinations to meet up.  Our Fare Prediction model will compare the latest prices
to see if you're getting a great deal and our Verdict analysis has got it's pulse on destination sentiment.
""")

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
    future_date = datetime.date.today() + datetime.timedelta(days=28)

    # Departure and return date input fields
    departure_date = (st.date_input('Travel Date', default_departure_date, min_value=datetime.date.today())).strftime("%d/%m/%Y")

    return_date_check = st.checkbox("Do you want to add a return date?", value=False)

    def get_return_date():
        if return_date_check == True:
            return_date = (st.date_input('Return Date', future_date)).strftime("%d/%m/%Y")
        else:
            return_date = ''

        return return_date

    return_date = get_return_date()

row2_11, row2_12,  row2_13,  row2_14 = st.columns((1,1,1,1))
with row2_11:
    st.write('')
with row2_12:
    st.write('')
with row2_13:
    # Continent selection
    continent_input = st.selectbox('Continent', ('Asia', 'Africa', 'Europe', 'North America', 'South America', 'Oceania'))

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

with row2_14:
    # Currency selection
    currency = st.selectbox('Currency', ('USD', 'AUD', 'NZD', 'JPY', 'EUR', 'INR'))


# ---------------------------
#        API Magic Area
# ---------------------------

    if st.button('SmackBang my Destinations'):
        # Spinner
        with st.spinner('Hold on while we search 1,000\'s of flights ...'):
            time.sleep(5)

        # Matches API query and output
        try:
            url = "https://smackbang-image-w76hg6ifha-ew.a.run.app/matches"

            headers = CaseInsensitiveDict()
            headers["accept"] = "application/json"

            query_string = {'origin_one':origin_one, 'origin_two':origin_two, 'departure_date':departure_date,
                            'continent':continent, 'return_date':return_date, 'currency':currency}

            result_matches = requests.get(url, headers=headers, params=query_string).json()
            matches_df = pd.DataFrame(result_matches)

        except:
            st.write('Well that\'s embarrassing. Looks like there\'s no flights on these dates.  Try a different date.')
            st.stop()


        # Fare Prediction Model
        try:
            new_list = [city_one, city_two]
            new_list2 = sorted(new_list, key=lambda x: (len(x), x))
            city_x = new_list2[1]
            city_y = new_list2[0]

            df1_formatted, df2_formatted = process_matches(matches_df,city_x,city_y)

            # Origin One
            df1_formatted.to_csv('data/df1.csv')
            data_processed_df1 = open('data/df1.csv')

            url = 'https://smackbang-image-w76hg6ifha-ew.a.run.app/predict'
            files = {
                    'file': ('data_processed.csv', data_processed_df1, 'multipart/form-data', {
                        'Expires': '0'
                    })
                }
            response_df1 = requests.post(url, files=files).json()

            # to import the preds into a df column:
            preds_df1 = pd.DataFrame(response_df1)

            # Origin Two
            df2_formatted.to_csv('data/df2.csv')
            data_processed_df2 = open('data/df2.csv')

            url = 'https://smackbang-image-w76hg6ifha-ew.a.run.app/predict'
            files_two = {
                    'file': ('data_processed.csv', data_processed_df2, 'multipart/form-data', {
                        'Expires': '0'
                    })
                }
            response_df2 = requests.post(url, files=files_two).json()

            # to import the preds into a df column:
            preds_df2 = pd.DataFrame(response_df2)

        except:
            st.write('Well that\'s embarrassing. Our model has gone to the pub for a drink.')
            st.stop()


        # Twitter API query
        try:
            url_twitter = "https://smackbang-image-w76hg6ifha-ew.a.run.app/twitter"

            matches_cities = matches_df.index.values
            keywords = ','.join(map(str,matches_cities))
            query_string_twitter = {'keywords':keywords}

            result = requests.get(url_twitter, headers=headers, params=query_string_twitter).json()
            twitter_df = pd.DataFrame(result)
            twitter_df['City'] = twitter_df['City'].str.title()
            twitter_df = twitter_df.set_index('City')
        except:
            st.write('Well that\'s embarrassing. One of your destinations doesn\'t like Twitter.  Try a different continent maybe.')
            st.stop()


# ---------------------------
#        User Output Header
# ---------------------------

st.markdown("""<hr style="height:4px;border:none;color:#161F6D;background-color:#161F6D;" /> """, unsafe_allow_html=True)

if origin_one_input == 'Origin' or origin_two_input == 'Origin' or matches_df.empty:
    st.header('So what Destinations are looking good ...')
    st.markdown('Enter your origins, travel dates and destination continent above to see exciting destinations to meet up.')
else:
    st.header(f'Destinations between {city_one} and {city_two} in {currency}')


row3_1, row3_2, row3_3, row3_4 = st.columns((1,1,1,1))

if origin_one_input == 'Origin' or origin_two_input == 'Origin' or matches_df.empty:
    st.write('')
else:
        with row3_1:
            st.markdown('Fair Prediction')
            st.write("🟢 Better than average. ✈️")
            st.write("🟠 Prices are about average. 😐")
            st.write("🔴 Worse than better. 🥵")

        with row3_2:
            st.markdown("Verdict")
            st.write("👍 Feedback tells us it's a good time to go.")
            st.write("👎 Better choose another destination.")

        with row3_3:
            st.write('')

        with row3_4:
            st.write('')


# ------------------------------------------------
#        User output table creation and formatting
# ------------------------------------------------

row4_1, row4_2 = st.columns((1,1))

with row4_1:

    if origin_one_input == 'Origin' or origin_two_input == 'Origin' or matches_df.empty:
        st.write('')

    else:
        def currency_con(currency):
            result = {
                    'USD': 0.013,
                    'AUD': 0.017,
                    'NZD': 0.019,
                    'JPY': 1.5,
                    'EUR': 0.011,
                    'INR': 1.0
                    }

            return result.get(currency)

        currency_factor = currency_con(currency)

        #currency_factor = 0.013

        def output_tables(matches_df):
            # 1.0 Copy Matches API dataframe required columns for user output
            output_df = matches_df.iloc[:,[0,1,14,12,13]]
            output_df = pd.merge(output_df, twitter_df, left_index=True, right_index=True)

            # 2.0 Currency format for columns that need it   {0, 1, 2}
            pd.set_option('display.max_colwidth', None)
            output_df.iloc[:,0] = output_df.iloc[:,0].apply(lambda x: f"{x:,.0f}")
            output_df.iloc[:,1] = output_df.iloc[:,1].apply(lambda x: f"{x:,.0f}")
            output_df.iloc[:,2] = output_df.iloc[:,2].apply(lambda x: f"{x:,.0f}")


            # 3.0 Get fare prediction model data and to dataframe {6, 7}
            output_df[f"{city_x}"] = preds_df1.values * currency_factor
            output_df[f"{city_y}"] = preds_df2.values * currency_factor
            output_df[f"{city_x}"] = output_df[f"{city_x}"].apply(lambda x: f"{x:,.0f}")
            output_df[f"{city_y}"] = output_df[f"{city_y}"].apply(lambda x: f"{x:,.0f}")

            # Add two columns for links to booking site {8, 9}
            output_df['Book1'] = f'from {city_two}' + '#' + output_df.iloc[:,3]
            output_df['Book2'] = f'from {city_one}' + '#' + output_df.iloc[:,4]

            def make_clickable(val):
                name, url = val.split('#')
                return f'<a href="{url}">{name}</a>'

            # Make columns with hyperlinks
            output_df['Book1'] = output_df['Book1'].apply(make_clickable)
            output_df['Book2'] = output_df['Book2'].apply(make_clickable)

            # Final output as a HTML table so links work
            output_df = output_df.iloc[:,[1,0,2,7,6,5,9,8]]
            output_df.columns=[f'{city_one}', f'{city_two}', 'Combined Fare', f'Predict {city_one}', f'Predict {city_two}', 'Verdict', 'Book', 'Book']
            output_df = output_df.to_html(escape=False)

            return st.write(output_df, unsafe_allow_html=True)

        output_tables(matches_df)


# ---------------------------
#        Arc Layer
# ---------------------------

with row4_2:

    if origin_one_input == 'Origin' or origin_two_input == 'Origin' or matches_df.empty:
        st.write('')

    else:
        # Get the data from the API query
        matches_map_query = matches_df.iloc[:,[16,17]]

        # Get the index names (i.e. destination cities)
        matches_names = matches_map_query.index.values

        # Origin One and Origin Two latitude and longitude coordinates
        origin_one_lat = airports.loc[airports['iata_code'] == origin_one, 'lat' ].to_string(index=False)
        origin_one_lon = airports.loc[airports['iata_code'] == origin_one, 'lon' ].to_string(index=False)
        origin_two_lat = airports.loc[airports['iata_code'] == origin_two, 'lat' ].to_string(index=False)
        origin_two_lon = airports.loc[airports['iata_code'] == origin_two, 'lon' ].to_string(index=False)

        # Origin One dataframe creation and population
        map_df = pd.DataFrame(matches_names, columns=['dest_city'])
        map_df['origin_one'] = origin_one
        map_df['lat_origin_one'] = origin_one_lat
        map_df['lon_origin_one'] = origin_one_lon

        map_df = pd.merge(map_df, matches_map_query.iloc[:,0], how='inner', left_on='dest_city', right_index=True)
        map_df = pd.merge(map_df, matches_map_query.iloc[:,1], how='inner', left_on='dest_city', right_index=True)

        # Origin Two dataframe creation and population
        map_df2 = pd.DataFrame(matches_names, columns=['dest_city'])
        map_df2['origin_one'] = origin_one
        map_df2['lat_origin_one'] = origin_one_lat
        map_df2['lon_origin_one'] = origin_one_lon

        map_df2 = pd.merge(map_df2, matches_map_query.iloc[:,0], how='inner', left_on='dest_city', right_index=True)
        map_df2 = pd.merge(map_df2, matches_map_query.iloc[:,1], how='inner', left_on='dest_city', right_index=True)

        # Start and end colours
        ORIGIN = [255, 0, 128]
        DESTINATION = [0, 200, 255]

        # The deck.gl ArcLayer
        st.pydeck_chart(pdk.Deck(
            map_provider='mapbox',
            map_style='mapbox://styles/mapbox/light-v10',
            tooltip = {
                    "text": "Destination: {dest_city}"
                    },
            initial_view_state = pdk.ViewState(
                latitude=0,
                longitude=100,
                bearing=0,
                pitch=45,
                zoom=1,
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
