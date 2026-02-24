import requests

class Cataas:
    url = "https://cataas.com/"
    def get_photo(self, text):
        try:
            response = requests.get(self.url + f"cat/says/{text}", params={'json': 'true'}, timeout=5)
            response.raise_for_status()
            return response.json()['url']
        except requests.exceptions.Timeout:
            return "Время ответа сервера превысило ожидаемое. Ошибка Timeout"
        except requests.exceptions.ConnectionError:
            return "Проблемы с интернет-соединением. Ошибка Connection_error"
        except requests.exceptions.HTTPError:
            return "Проблемы с сервером. Ошибка Server_error"
        except requests.exceptions.RequestException:
            return "Ошибка Exception"
