
from datetime import date


def get_date(entry):
    # extract date
    dt = entry['dt']
    dt = date.fromtimestamp(dt)
    return str(dt)


def get_temp_print(entry):
    # extract temp in f

    temp_k = entry['main']['temp']
    temp_f = temp_k * (9/5) - 459.67
    temp_f = round(temp_f, 1)
    temp_f_wUnit = f'{temp_f} F'
    return temp_f_wUnit


def get_weather_main(entry):
    # get weather main

    return entry['weather'][0]['main']


def get_weather_desc(entry):
    # get weather description

    return entry['weather'][0]['description']
