import datetime
import os
import time
from functools import wraps
from random import randint
from PIL import Image
import urllib.request
import requests
import json
import imdb_api_key
import yagmail
import ResizeImg
import csv
from csv import reader

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


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
    year = datetime.date.today().year
    # Тепрь нужно из списка со словарями удалить те, что не подходят нам по рейтингу
    # И вот тут как раз главная проблема. Лист со словарями по мере удаления уменьшается а мы то считаем с 1 до 100
    # Поэтому просто ut of range . Нужно каждый последующий фильм или через next доставать или как-то еще
    for count, i in enumerate(x):
        try:
            # Сделал проверку на вышел ли фильм или еще нет
            if int(i['year']) < 2018 or int(i['year']) > year:
                del x[count]
            elif float(i['imDbRating']) < 6.5:
                del x[count]
            elif int(i['imDbRatingCount']) < 20000:
                del x[count]
        except ValueError:
            del x[count]
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
    # TODO Здесь необходимо реализовать алгоритм запоминающий какие фильмы мы уже отправляли что не было потворов
    y = filter_by_rating()
    # Делаем z словарем
    def check_for_repeat():
        # Мы получаем фильм
        z = film(y[randint(1, len(y))]['id'], False)

        # Присваиваем название переменной чтобы потом если что его записать
        film_id = [z['fullTitle']]

        #Открываем файл чтобы чекнуть есть ли там фильм
        with open('already_added_films.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for i in csv_reader:
                if film_id == i:
                    print('Этот фильм уже был отправлен')
                    check_for_repeat()
            with open('already_added_films.csv', 'a', newline='', encoding='utf-8') as csvfile:
                x = csv.writer(csvfile)
                x.writerow(film_id)
        return z

    return check_for_repeat()


@timeit
def send_email():
    x = complete_dict_with_filtered_films()

    def stars_img() -> list:
        return [i['image'] for i in x['actorList'] if i['name'] in x['stars']]

    stars_img_lst = stars_img()
    yag = yagmail.SMTP(user='tet.yag2022', password='jmzbgylqzquygkih')
    """Код ниже отправляет email. Я создал ящик на gmail чтобы отправлять всякое. Мне понадобится отправлять письмо в
    определенном формате чтобы это выглядело классно. Т е постер фильма, каст, актеры и т.п."""
    ResizeImg.ResizeImg.resize_complete(x['image'])
    k = ''

    for url in stars_img_lst:
        k += f'<img src="{url}" width="150" height="200">'
    content = [
        f'<h2>{x["fullTitle"]}\n</h2>', yagmail.inline("./resized_poster.jpg"),
        f'\n<i>{x["plot"]}</i>\n'
        f'\n<b>Cast: </b>{x["stars"]}\n'
        # Вот сюда хотелось бы вставить фотки актеров
        f'{k}'
        f'\n<b>Genres: </b>{x["genres"]}'
        f'\n<b>Trailer: </b>{x["videoUrl"]}'
        f'\n<b>Companies: </b>{x["companies"]}'
        f'\n<b>imDbRating: </b>{x["imDbRating"]}'
        f'\n<b>imDbRatingVotes: </b>{x["imDbRatingVotes"]}'
        f'\n<b>metacriticRating: </b>{x["metacriticRating"]}'
        f'\n<b>boxOffice: </b>Budget: {x["boxOffice"]["budget"]}']

    # В примере ниже всё работает и отправляет фотку как бы при помощи html
    yag.send('alamana13@mail.ru', 'Film', content)
    print('Cообщение отправлено')
    os.remove('resized_poster.jpg')


if __name__ == '__main__':
    send_email()
    # while True:
    #     try:
    #         send_email()
    #         time.sleep(60)
    #     except Exception as e:
    #         print(f'Oops we hava exception ---> {e}')
    #         continue


