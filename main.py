import time
from random import randint

import requests
import json
import imdb_api_key
import yagmail


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# Самый первый мой запрос в базу который вытаскивает популярные фильмы
def request_popular():
    url = f"https://imdb-api.com/en/API/MostPopularMovies/{imdb_api_key.api_key}"
    payload, headers = {}, {}

    # Создаем объект response с json внутри
    response = requests.request("GET", url, headers=headers, data=payload)

    # Далее происходит перевод текста в кодировку
    json_data = response.text.encode('utf8')

    # Дальше мы создаем pytjon объект из изначального json
    json_object = json.loads(json_data)

    # #Дальнейшая строчка уже не нужна, но так для понимания - это красивое отображение json столбиков в виде str
    # json_formatted_str = json.dumps(json_object, indent=1)

    # Эти два цикла как раз печатают все фильмы из запроса по условию
    # y = json.loads(json_data)
    return json_object


def filter_by_rating() -> dict:
    # Делается запрос
    x = request_popular()
    # Переходим к самим словарям
    x = x['items']
    # Тепрь нужно из списка со словарями удалить те, что не подходят нам по рейтингу
    for i in range(len(x)):
        try:
            if float(x[i]['imDbRating']) < 6.5 or int(x[i]['imDbRatingCount']) < 50000 or int(x[i]['year']) < 2018:
                del x[i]
        except Exception as e:
            # print(f'Oops we have exception {e}')
            continue
    return x


def film(id_of_film: str, str_or_dict) -> dict:
    """
    :param id_of_film: id of film like 'tt1649418'
    :param str_or_dict: Bool
    :return: pretty loking json in str format (if str_or_dict == True) or dict (if str_or_dict == False)
    """
    url = f"https://imdb-api.com/en/API/Title/{imdb_api_key.api_key}/{id_of_film}"
    url_video = f'https://imdb-api.com/en/API/YouTubeTrailer/{imdb_api_key.api_key}/{id_of_film}'
    payload, headers = {}, {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_video = requests.request("GET", url_video, headers=headers, data=payload)

    json_data = response.text.encode('utf8')
    json_data_video = response_video.text.encode('utf8')

    # Дальше мы создаем pytjon объект из изначального json
    json_object = json.loads(json_data)
    json_object_with_video = json.loads(json_data_video)

    # #Дальнейшая строчка уже не нужна, но так для понимания - это красивое отображение json столбиков в виде str
    json_formatted_str = json.dumps(json_object, indent=1)

    # Добавим ссылку на видео-трейлер в словарь
    film_dict = json_object
    film_dict['videoUrl'] = json_object_with_video['videoUrl']

    return json_formatted_str if str_or_dict else film_dict


def show(x: dict):
    for key, value in x.items():
        try:
            if key in ('id', 'fullTitle', 'year', 'image', 'releaseDate', 'runtimeMins', 'plot', 'awards', 'directors',
                       'stars', 'genres', 'companies', 'languages', 'contentRating', 'imDbRating', 'imDbRatingVotes',
                       'metacriticRating', 'trailer', 'boxOffice', 'videoUrl', 'starList'):
                print(f'{key} ---> {value}')
        except Exception as e:
            print(f'Ooops where have exception {e}')

def complete_dict_with_filtered_films() -> dict:
    complete_dict = {}
    y = filter_by_rating()
    #Делаем z словарем
    z = film(y[randint(1, len(y))]['id'], False)
    return z

def send_email():
    x = complete_dict_with_filtered_films()
    yag = yagmail.SMTP(user='tet.yag2022', password='jmzbgylqzquygkih')
    """Код ниже отправляет email. Я создал ящик на gmail чтобы отправлять всякое. Мне понадобится отправлять письмо в
    определенном формате чтобы это выглядело классно. Т е постер фильма, каст, актеры и т.п."""
    image = x["image"]
    context = [f'Посмотри фильм на вечер\n<img src="{image}"/>\n {x["fullTitle"]}\n{x["plot"]}\n{x["stars"]}\n{x["videoUrl"]}']
    # В примере ниже всё работает и отправляет фотку как бы при помощи html
    yag.send('alamana13@mail.ru', 'Film', context)
    print('Cообщение отправлено')

# # Проверка работоспособности
# print(show(film('tt1649418', False)))



# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     popular()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

send_email()