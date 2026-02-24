from Cataas import Cataas
from yandex_disc import YandexDisc


def backup():
    print('Программа делает резервное копирование картинок с сайта Cataas.com на Яндекс.Диск.')
    token = input('Введите свой токен для доступа к функциям диска: ')
    name_file = input('Как подпишем картинку?: ')
    ya_disc = YandexDisc(token, name_file)

    # Получаем ссылку на файл: фото кошки с подписью
    rnd_cat = Cataas().get_photo(name_file)
    ya_disc.upload_file(rnd_cat)


if __name__ == "__main__":
    backup()
