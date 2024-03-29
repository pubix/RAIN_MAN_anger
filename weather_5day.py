import argparse


import requests

import weath_json_parse


def city_flag_check(arg_output):
    """[Subfunction designed to identify whether or not any flags have been selected]

    Arguments:
        arg_output {[ArgParserObject]} -- [Command line arguments]
    """

    city_lst = ['sandiego', 'sanfrancisco', 'paloalto', 'houston', 'seattle']
    cityflag = True
    for city in city_lst:
        if getattr(arg_output, city):  # translats
            cityflag = False
    return(cityflag)


def get_zip(arg_output):
    """[The purpose of this function is to get zip codes associated to cities selected for weather]

    Arguments:
        arg_output {[str]} -- [From Arg parser]
    """
    ziplst = []

    if arg_output.all or city_flag_check(arg_output):
        print('Upcoming rain for Houston, South SF, Palo Alto, San Diego, and Seattle:')
        ziplst = [92116, 98109, 77030, 94080, 94301]

    else:
        if arg_output.sandiego:
            print('Upcoming rain for San Diego:')
            ziplst.append(92116)
        if arg_output.sanfrancisco:
            print('Upcoming rain for South SF:')
            ziplst.append(94080)
        if arg_output.paloalto:
            print('Upcoming rain for Palo Alto:')
            ziplst.append(94301)
        if arg_output.houston:
            print('Upcoming rain for Houston:')
            ziplst.append(77030)
        if arg_output.seattle:
            print('Upcoming rain for Seattle:')
            ziplst.append(98109)
    return (ziplst)


def get_args():
    """[This function is designed to get the cities for weather anlaysis.]
    """
    parser = argparse.ArgumentParser(
        description='5 day weather forecaster')
    parser.add_argument('-a', '--all',
                        action='store_true', help='All Cities')
    parser.add_argument('-sd', '--sandiego',
                        action='store_true', help='San Diego Only')
    parser.add_argument('-sf', '--sanfrancisco',
                        action='store_true', help='South San Francisco Only')
    parser.add_argument('-pa', '--paloalto',
                        action='store_true', help='Palo Alto Only')
    parser.add_argument('-hou', '--houston',
                        action='store_true', help='Houston Only')
    parser.add_argument('-sea', '--seattle',
                        action='store_true', help='Seattle Only')
    args = parser.parse_args()
    return (args)


def get_api_key():
    # to retrieve API key from text file
    with open('weather_api_key.txt', 'r') as file_obj:
        api_key = file_obj.read()
        return(str(api_key))

    #! TODO
    #! Try to implement method to pull api key from environment within os

    # import os

    # try:
    #     api_key = os.environ.get('WEATHER_API')
    #     return (api_key)
    # except:  # find detailed error
    #     print('No Weather API key in environment')
    #     pass


def rain_day_printer(rainday_lst):
    """to print out rainy days per city"""
    for d_ate in rainday_lst:
        print(d_ate)


def get_rain_days(nested_dict):
    rain_days = []
    for res in nested_dict:
        if 'rain' in res['weather']['weather_main'].lower():
            rain_date = str(res['dt'])
            city = res['city']
            sentence = f'Rain in {city} {rain_date}'
            if sentence not in rain_days:
                rain_days.append(sentence)
    return(rain_days)


def weather_percity(city, data_json):
    results = []
    for i, day in enumerate(data_json['list']):

        dt = weath_json_parse.get_date(day)
        temp_f_wUnit = weath_json_parse.get_temp_print(day)
        weather_main = weath_json_parse.get_weather_main(day)
        weather_desc = weath_json_parse.get_weather_desc(day)

        results.append({
            'city': city,
            'weather': {
                'weather_main': weather_main,
                'weather_desc': weather_desc,
            },
            'temp': temp_f_wUnit,
            'dt': dt
        })
    return results


def five_day_rain_finder(listofzips):
    if listofzips is None:
        print('No city selected.')
        return
    else:
        api_key = get_api_key()

        for city in listofzips:

            country_code = 'us'

            # to fetch from weather api directly

            # current weather
            # url = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&APPID={api_key}'

            # 5 day forecast
            url = f'http://api.openweathermap.org/data/2.5/forecast?zip={city},{country_code}&APPID={api_key}'

            data = requests.get(url)
            data_json = data.json()

            '''
            # temp use saved file
            with open('5day_weather.json', 'r') as f:
                data_json = json.load(f)
            '''
            # print(data_json)

            # main function

            city = data_json['city']['name']

            results = weather_percity(city, data_json)
            rain_days = get_rain_days(results)
            rain_day_printer(rain_days)


if __name__ == "__main__":
    arg_output = get_args()
    zip_lst = get_zip(arg_output)
    five_day_rain_finder(zip_lst)
