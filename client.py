import requests
from requests import RequestException


class ClientException(Exception):
    pass


class Client:
    def __init__(self, endpoint: str, token: str):
        self.endpoint = endpoint
        self.token = token
        self.format = 'json'

    def get_timezones(self) -> dict:
        try:
            params = self.__get_protocol_params() | {}
            res = requests.get(self.endpoint + '/list-time-zone', params=params)

            data = res.json()

            if data['status'] != 'OK':
                raise ClientException(data['message'])

            return data['zones']
        except RequestException as ex:
            raise ClientException(str(ex))

    def get_timezone_details(self, name: str) -> dict:
        try:
            params = self.__get_protocol_params() | {
                'by': 'zone',
                'zone': name
            }

            res = requests.get(self.endpoint + '/get-time-zone', params=params)

            data = res.json()

            if data['status'] != 'OK':
                raise ClientException(data['message'])

            return data
        except RequestException as ex:
            raise ClientException(str(ex))

    def __get_protocol_params(self) -> dict:
        return {
            'key': self.token,
            'format': self.format
        }
