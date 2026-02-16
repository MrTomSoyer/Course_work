import requests

class Cataas:
    url = "https://cataas.com/"

    def get_photo(self, text):
        href = ''
        response = requests.get(self.url + f"cat/says/{text}", params={'json': 'true'})
        if response.status_code == 200:
            href = response.json()['url']
        else:
            raise RuntimeError(f'{response.status_code}')
        return href
