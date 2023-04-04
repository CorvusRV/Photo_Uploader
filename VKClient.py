import requests


class VKClient:
    url = "https://api.vk.com/"
    url_photo = f"{url}method/photos.get"

    def __init__(self, vk_token: str, api_version: str = '5.131'):
        self.token = vk_token
        self.api_version = api_version
        self.params = {'access_token': self.token, 'v': self.api_version}

    def photo_uploader(self, user_id, count, rev):
        """запрос json с фотографиями альбома"""
        params = {'owner_id': user_id,
                  'album_id': 'profile',
                  'extended': count,
                  'rev': rev
                  }
        res = requests.get(self.url_photo, params={**self.params, **params})
        return res.json()

    @staticmethod
    def photo_url(photo_json, numb):
        """определение url фотографии с максимальным размером и кол-во лайков у фотографии"""
        photo_sizes = photo_json["sizes"]
        photo_likes = photo_json["likes"]["count"]
        photo_sizes = sorted(photo_sizes, key=lambda x: (x['height'], x['width'], x['type']), reverse=True)
        return numb, photo_sizes[0]['url'], photo_sizes[0]["type"], photo_likes

    @staticmethod
    def photo_count(json, amount):
        """определение кол-ва обрабатываемых фотографий в альбоме"""
        photo_amount = len(json["response"]["items"])
        if 0 < amount <= photo_amount:
            return amount
        else:
            print("\033[31m{}".format(f"{amount} фотографий скачать невозможно, будет скачано {photo_amount}"))
            return photo_amount
