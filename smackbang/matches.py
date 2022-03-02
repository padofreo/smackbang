import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict

def get_matches(origin_one, origin_two, departure_date, return_date="", currency='USD', continent='AS'):
    '''
    Required arguments: origin_one, origin_two and contintent
    Optional argugments: return_date
    Returns df  index=['cityTo'],
    columns=[origin_one,origin_two,origin_one_price,origin_two_price,combined_price
    '''
    url = "https://tequila-api.kiwi.com/v2/search"
    airports_df = pd.read_csv('../raw_data/airport_codes.csv')
    origins = f'{origin_one},{origin_two}'
    destinations_ser = airports_df[airports_df['continent']==continent]['iata_code'].dropna()
    destinations_list = []

    for code in destinations_ser:
        destinations_list.append(code)

    if origin_one in destinations_list:
        destinations_list.remove(origin_one)

    if origin_two in destinations_list:
        destinations_list.remove(origin_two)

    fly_to = ','.join(destinations_list)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["apikey"] = "Ul0VynVifRdwPUGTkFU_Btfro1vyewb7"

    query_string = {'fly_from':origins, 'fly_to':fly_to,
                'date_from':departure_date, 'date_to':departure_date,'return_from':'','return_to':'',
               'adults':1, 'children':0,'selected_cabins':'M','adult_hold_bag':1,'adult_hand_bag':1,
               "curr":'USD', 'limit':1000}

    resp = requests.get(url, headers=headers, params=query_string)
    print(origins)
    print(type(origins))
    print(departure_date)
    print(type(departure_date))
    print(fly_to)
    print(type(fly_to))

    #print(resp.status_code)


if __name__ == "__main__":

    get_matches('NRT','SYD','01/04/2022')
