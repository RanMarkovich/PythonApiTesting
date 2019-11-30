import requests
from pytest import fixture

from OpenWeather.open_weather_service import OpenWeather


# kfar sava city name: Kfar%20Saba
# kfar saba city id: 294514
# kfar saba coordinates: lon:34.91 , lat:32.18
# app_id: 7575e7608cc6fa2587b22b386c5c64c8

@fixture
def open_weather_service():
    return OpenWeather()


def test_weather_by_city_name(open_weather_service):
    r = open_weather_service.get_city_weather(by='name', city_name='Kfar%20Saba')
    city_name = r.json()['name']
    city_id = r.json()['id']
    assert city_name == 'Kfar Saba', f'Expected city name to be Kfar Saba, instead got: {city_name}'
    assert city_id == 294514, f'Expected city id to be 294514, instead got: {city_id}'
    weather = r.json()['weather']
    assert weather is not None, f'Got an empty weather parameter: {r.text}'


def test_weather_by_city_name_and_country_code(open_weather_service):
    r = open_weather_service.get_city_weather(by='name and country code', city_name='Kfar%20Saba', country_code='il')
    city_name = r.json()['name']
    city_id = r.json()['id']
    assert city_name == 'Kfar Saba', f'Expected city name to be Kfar Saba, instead got: {city_name}'
    assert city_id == 294514, f'Expected city id to be 294514, instead got: {city_id}'
    weather = r.json()['weather']
    assert weather is not None, f'Got an empty weather parameter: {r.text}'


def test_weather_by_city_id(open_weather_service):
    r = open_weather_service.get_city_weather(by='id', city_id='294514')
    city_name = r.json()['name']
    city_id = r.json()['id']
    assert city_name == 'Kfar Saba', f'Expected city name to be Kfar Saba, instead got: {city_name}'
    assert city_id == 294514, f'Expected city id to be 294514, instead got: {city_id}'
    weather = r.json()['weather']
    assert weather is not None, f'Got an empty weather parameter: {r.text}'


def test_weather_by_geographic_coordinates(open_weather_service):
    r = open_weather_service.get_city_weather(by='geographic coordinates', lat_lon=['32.18', '34.91'])
    city_name = r.json()['name']
    city_id = r.json()['id']
    assert city_name == 'Kfar Saba', f'Expected city name to be Kfar Saba, instead got: {city_name}'
    assert city_id == 294514, f'Expected city id to be 294514, instead got: {city_id}'
    weather = r.json()['weather']
    assert weather is not None, f'Got an empty weather parameter: {r.text}'


def test_invalid_city_name(open_weather_service):
    r = open_weather_service.get_city_weather(by='name', city_name='Invalid')
    assert r.status_code == 404 and r.json()[
        'message'] == 'city not found', f'Expected error code 404, instead got: {r.text}'


def test_valid_city_name_id_and_wrong_country_code(open_weather_service):
    r = open_weather_service.get_city_weather(by='name and country code', city_name='Kfar%20Saba', country_code='us')
    assert r.status_code == 404 and r.json()[
        'message'] == 'city not found', f'Expected error code 404, instead got: {r.text}'


def test_invalid_city_id(open_weather_service):
    r = open_weather_service.get_city_weather(by='id', city_id='999999')
    assert r.status_code == 404 and r.json()[
        'message'] == 'city not found', f'Expected error code 404, instead got: {r.text}'


def test_invalid_coordinates(open_weather_service):
    r = open_weather_service.get_city_weather(by='geographic coordinates', lat_lon=['lat', 'lon'])
    assert r.status_code == 400 and r.json()[
        'message'] == 'undefined is not a float', f'Expected error code 400, instead got: {r.text}'
    r = open_weather_service.get_city_weather(by='geographic coordinates', lat_lon=['99', '0.0'])
    assert r.status_code == 400 and r.json()[
        'message'] == '99 is not a float', f'Expected error code 400, instead got: {r.text}'
    r = open_weather_service.get_city_weather(by='geographic coordinates', lat_lon=['0.0', '999.0'])
    assert r.status_code == 400 and r.json()[
        'message'] == '999.0 is not a float', f'Expected error code 400, instead got: {r.text}'


def test_wrong_coordinates(open_weather_service):
    r = open_weather_service.get_city_weather(by='geographic coordinates', lat_lon=['0.0', '0.0'])
    assert r.status_code == 200, f'Expected to get status code 200, instead got: {r.text}'
    city_name = r.json()['name']
    city_id = r.json()['id']
    assert city_name != 'Kfar Saba', f'Expected city name to be Kfar Saba, instead got: {city_name}'
    assert city_id != 294514, f'Expected city id to be 294514, instead got: {city_id}'
    weather = r.json()['weather']
    assert weather is not None, f'Got an empty weather parameter: {r.text}'
