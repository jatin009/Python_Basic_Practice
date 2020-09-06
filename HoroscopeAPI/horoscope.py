import requests
import json
from pprint import pprint

"""
A program to find out if the girl is manglik or not.
And how is the horoscope match with Jatin (his details hardcoded here).
It uses 2 APIs:
    - api.opencagedata.com: for finding the latitude and longitude of the birth place
    - api.prokerala.com:    for determining if the girl is manglik or not and how's the horoscope match

Input datetime in format: 01-06-1991T12:06:00
Input place:              New Delhi, India
"""

class GeoDetails:
    URL = "https://api.opencagedata.com/geocode/v1/json"
    KEY = '138f1a2cbb474f7b8ced20ecb5f75a46'


class HoroscopeDetails:
    MANGLIK_URL = 'https://api.prokerala.com/v1/astrology/manglik'
    KUNDLI_MILAN_URL = 'https://api.prokerala.com/v1/astrology/kundli-matching'
    HEADERS = {
        "Authorization": "Bearer 5fda56b5eba8b8980fb0e1fafbef94e2d7e11a17b2e36963337309c4c08852c3",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    AshtaKoot = {
        'varna': {'Area':'Work', 'TotalPoint':1},
        'vasya': {'Area':'Dominance', 'TotalPoint':2},
        'tara': {'Area':'Destiny', 'TotalPoint':3},
        'yoni': {'Area':'Mentality', 'TotalPoint':4},
        'graha_maitri': {'Area':'Compatibility', 'TotalPoint':5},
        'gana': {'Area':'Nature', 'TotalPoint':6},
        'bhakoot': {'Area':'Love', 'TotalPoint':7},
        'nadi': {'Area':'Health', 'TotalPoint':8}
    }


def get_formatted_datetime(date_time_birth):
    date, time  = date_time_birth.split('T')
    d, m, y = date.split('-')
    dob = f'{y}-{m}-{d}'
    return f"{dob}T{time}"


def get_place_lat_lng(location):
    geo_resp = requests.get(GeoDetails.URL, params={ 'key':GeoDetails.KEY, 'q':location })
    geo_data = geo_resp.json()
    return geo_data['results'][0]['geometry']['lat'], geo_data['results'][0]['geometry']['lng']


def output_horoscope_match(date_time_birth, *args):
    data = {
        'ayanamsa': '1',        # always 1
        'datetime': f'{date_time_birth}+05:30',    # +05:30 as Time zone offset of IST Indian is UTC+05:30.
        'coordinates': f'{args[0]},{args[1]}'
    }
    horoscope_resp = requests.get(HoroscopeDetails.MANGLIK_URL, headers=HoroscopeDetails.HEADERS, params=data)
    data = horoscope_resp.json()
    is_manglik = "Manglik" if data['response']['result']['manglik_status'] else "Non-manglik"
    print("\n######### Here are the details #########\n")
    print(f"The girl is {is_manglik}\n")

    params = {
        "ayanamsa": "1",
        "bride_dob": f'{date_time_birth}+05:30',
        "bride_coordinates": f'{args[0]},{args[1]}',
        "bridegroom_dob": "1991-06-01T12:06:00+05:30",      # hard-coding my birth time
        "bridegroom_coordinates": "28.6138954,77.2090057",  # hard-coding my place of birth
    }
    horoscope_resp = requests.get(HoroscopeDetails.KUNDLI_MILAN_URL, headers=HoroscopeDetails.HEADERS, 
    params=params)
    data = horoscope_resp.json()

    print(data['response']['result']['message'])
    print(f"{data['response']['result']['total_point']}/36")

    for k, v in HoroscopeDetails.AshtaKoot.items():
        print(f"{v['Area']}: \t\t\t{data['response']['result'][k]['point']}/{v['TotalPoint']}".rjust(25))

    print(f"\n{data['response']['result']['sub_message'][0]}\n")


datetime_birth = get_formatted_datetime(input("Enter the date & time of girl's birth (DD-MM-YYYYTHH:MM:SS): "))
lat, lng = get_place_lat_lng(input("Enter the birth place of girl: "))
output_horoscope_match(datetime_birth, lat, lng)
