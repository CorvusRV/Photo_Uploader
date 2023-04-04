import requests


class YDClient:
    url = "https://cloud-api.yandex.net/v1/disk"
    url_res = f"{url}/resources"
    url_res_up = f"{url_res}/upload"

    def __init__(self, yad_token: str):
        self.headers = {"Content-Type": "application/json",
                        'Accept': 'application/json',
                        "Authorization": f"OAuth {yad_token}"}

    def connection_test(self):
        """Метод проверяет соединение с сервером"""
        resp = requests.get(self.url, headers=self.headers)
        return resp.status_code

    def create_folder(self, folder_name):
        """Создание альбома для фотографий на Яндекс Диске. \n path: Путь к создаваемой папке."""
        params = {"path": folder_name}
        requests.put(self.url_res, headers=self.headers, params=params)

    def download_photo(self, photo_name, folder_name):
        """запрашивает url для загрузки и загружает файл"""
        params = {"path": f"{folder_name}/{photo_name}"}
        photo_url = requests.get(self.url_res_up, headers=self.headers, params=params).json()
        requests.put(photo_url['href'], data=open(f"{photo_name}", 'rb'), headers=self.headers)
