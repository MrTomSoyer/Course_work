import json
import requests

class YandexDisc:
    main_url = "https://cloud-api.yandex.net/"
    add_url = "v1/disk/resources"
    url = main_url + add_url
    params = {
        "path": "PD-144"
    }


    def __init__(self, token, name_file):
        self.token = token
        self.name_file = name_file
        self.headers = {
            "Authorization": f"OAuth {self.token}"
        }


    def create_folder(self):
        response = requests.put(self.url, params=self.params, headers=self.headers)
        if response.status_code in (200, 201):
            print(f"Создана папка '{self.params["path"]}'")


    def async_done(self, response):
        op_item = response.json()['href']
        while True:
            async_done = requests.get(op_item, headers=self.headers)
            if async_done.status_code == 200:
                break


    def delete_folder(self):
        response = requests.delete(self.url, params=self.params, headers=self.headers)
        if response.status_code in (204, 200, 202):
            if response.status_code == 202:
                self.async_done(response)
                print("Папка удалена с Яндекс.Диска")
        elif response.status_code == 404:
            print(f"Не удалось найти папку '{self.params["path"]}")
        else:
            print("Ошибка при удалении папки с Яндекс.Диска")


    def upload_file(self, url_download_file):
        self.create_folder()
        params = {
            'path': f"{self.params["path"]}/{self.name_file}.jpg",
            'url': url_download_file
        }
        # Проверяем на наличие файла с таким же именем на Яндекс.Диске
        response_name = requests.get(self.url, params={'path': params['path']}, headers=self.headers)
        if response_name.status_code == 200:
            copy_name = response_name.json()['name'][:-4]
            if copy_name == self.name_file:
                self.info(params['path'])
                print("Фото с такой подписью уже есть на Яндекс.Диске")
        elif response_name.status_code == 404:
            response_async = requests.post(self.url + "/upload", params=params, headers=self.headers)
            if response_async.status_code == 202:
                self.async_done(response_async)
                self.info(params['path'])
                print("Копия создана и загружена на Яндекс.Диск")
        else:
            print("Ошибка резервного копирования файла")

    def info(self, file):
        response = requests.get(self.url,params={'path': file}, headers=self.headers)
        if response.status_code == 200:
            file_info = {'Размер загруженного файла': f'{response.json()["size"]}'}
            with open("Размер загруженного файла.json", "w", encoding='utf-8') as f:
                json.dump(file_info, f, ensure_ascii=False, indent=4)
            return 'Файл создан'
        elif response.status_code == 401:
            return 'Неверно ввели токен. Авторизация не прошла'
        else:
            return "Ошибка"


    def get_all_files(self):
        list_of_files = []
        file = {'Список файлов': list_of_files}
        response = requests.get(self.url + '/files', headers=self.headers)
        if response.status_code == 200:
            for item in response.json()['items']:
                file['Список файлов'].append({'Название файла': item['name'], 'Размер файла в байтах': item['size']})
            with open("Список файлов.json", "w", encoding='utf-8') as f:
                json.dump(file, f, ensure_ascii=False, indent=4)
            return 'Файл создан'
        elif response.status_code == 401:
            return 'Неверно ввели токен. Авторизация не прошла'
        else:
            return "Ошибка"