import os.path
import urllib.request
from tqdm import tqdm
from VKClient import VKClient
from YDClient import YDClient
from sistem import yd_token, vk_token


class Uploader:

    def __init__(self):
        self.user_id = self.getting_user_id()  # id человека, с чьего альбома будут скачиваться фотографии
        self.count = self.number_of_downloaded_photos()  # кол-во скачиваемых фотографий
        self.reverse = self.reverses()
        self.folder_name = self.folder_name()  # название альбома на яд

    def getting_user_id(self):
        """запрос id пользователя VK"""
        user_id = input("Введите цифровое id пользователя vk: ")
        if user_id.isdigit():
            return user_id
        print("Данный id не подходит, попробуйте ещё раз")
        return self.getting_user_id()

    @staticmethod
    def number_of_downloaded_photos():
        """кол-ва скачиваемых фотографий"""
        number_photos = input("Сколько фотографий необходимо скачать: ")
        if number_photos.isalpha():
            number_photos = 1
            print("Данные введены не корректно, будет скачана 1 фотография")
        return int(number_photos)

    @staticmethod
    def reverses():
        """запрос порядка скачивания фотографий"""
        rev = input("Сначала скачать новые фотографии (да/нет): ").lower()
        if rev == "да" or rev == "1":
            return 1
        return 0

    @staticmethod
    def folder_name():
        """запрос названия альбома на яндекс диске"""
        folder_name = input("Введите название альбома для фотографий: ")
        return folder_name


def name_availability_check(func):
    name_dict = {}

    def wrapper(name):
        if name not in name_dict:
            name_dict[name] = 1
        else:
            name_dict[name] += 1
            name = f'{name}_{name_dict[name]}'
        return func(name)

    return wrapper


@name_availability_check
def name_of_the_photograph(name):
    return name + 'jpg'


if __name__ == '__main__':
    uploader = Uploader()
    vkclient = VKClient(vk_token)
    ydclient = YDClient(yd_token)
    json = vkclient.photo_uploader(user_id=uploader.user_id, count=uploader.count, rev=uploader.reverse)
    test = ydclient.connection_test()
    if 'error' in json or test != 200:
        print("\033[31m{}".format("Произошла ошибка, попробуйте перезапустить программу"))
        if 'error' in json:
            print("\033[31m{}".format(f"Не удалось загрузить фотографии с аккаунта {uploader.user_id}"))
        if test != 200:
            print("Сервер Яндекс не доступен")
    else:
        count = vkclient.photo_count(json, uploader.count)
        print("\033[31m{}".format("Соединение установлено"))
        ydclient.create_folder(uploader.folder_name)  # создает папку на ЯД
        for i in tqdm(range(count), ncols=50):
            photo_json = json["response"]["items"][i]
            numb, url_photo, sizes, photo_likes = vkclient.photo_url(photo_json, i)
            photo_likes = str(photo_likes)
            photo_name = name_of_the_photograph(str(photo_likes))
            urllib.request.urlretrieve(url_photo, photo_name)  # загрузка фотографии из VK
            ydclient.download_photo(photo_name=photo_name, folder_name=uploader.folder_name)  # загрузка на ЯД
            os.remove(photo_name)  # удаление фотографии с компьютера
        print("\033[31m{}".format("Загрузка завершена"))
