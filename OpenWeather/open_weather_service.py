import requests


class OpenWeather:
    path = 'http://api.openweathermap.org/data/2.5/weather?'
    app_id = '7575e7608cc6fa2587b22b386c5c64c8'

    def __init__(self, city_name=None, city_id=None, lon=None, lat=None):
        self.city_name = city_name
        self.city_id = city_id
        self.lon = lon
        self.lat = lat

    def get_city_weather(self, by, city_name=None, country_code=None, city_id=None, lat_lon=None):
        if by == 'name':
            r = requests.get(f'{self.path}q={city_name}&appid={self.app_id}')
            assert r.status_code == 200 or (
                    404 and r.json()['message'] == 'city not found'), f'Got unexpected status code: {r.text}'
            return r
        elif by == 'name and country code':
            r = requests.get(f'{self.path}q={city_name},{country_code}&appid={self.app_id}')
            assert r.status_code == 200 or (404 and r.json()[
                'message'] == 'city not found'), f'Got unexpected status code: {r.text}'
            return r
        elif by == 'id':
            r = requests.get(
                f'{self.path}id={city_id}&appid={self.app_id}')
            assert r.status_code == 200 or (
                    404 and r.json()['message'] == 'city not found'), f'Got unexpected status code: {r.text}'
            return r
        elif by == 'geographic coordinates':
            r = requests.get(
                f'{self.path}lat={lat_lon[0]}&lon={lat_lon[1]}&appid={self.app_id}')
            assert r.status_code == 200 or 400, f'Got unexpected status code: {r.text}'
            return r
