import time

import requests
import json


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def request():
    url = "https://imdb-api.com/en/API/MostPopularMovies/k_1cob5uy7"
    payload = {}
    headers = {}
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


def popular():
    y = request()
    print(f'длина {y}', len(y))
    count = 0
    for i in range(1, len(y)):
        if isfloat(y[i]['imDbRating']):
            try:
                if float(y[i]['imDbRating']) > 5.5 and int(y[i]['imDbRatingCount']) > 50000:
                    print(f'№{count}')
                    for key, value in y[i].items():
                        if key not in ['id', 'rankUpDown', 'rank', 'title']:
                            print(f'{key} ---> {value}')
                    print()
                    count += 1
            except Exception as e:
                print(f"something went wrong! - {e} ---> {y[i]['imDbRating']}")
                time.sleep(5)
                continue
        else:
            continue


# API key k_1cob5uy7

def film(id_of_film: str, str_or_dict) -> str:
    """
    :param id_of_film: id of film like 'tt1649418'
    :param str_or_dict: Bool
    :return: pretty loking json in str format (if str_or_dict == True) or dict (if str_or_dict == False)
    """
    url = f"https://imdb-api.com/en/API/Title/k_1cob5uy7/{id_of_film}"
    url_video = f'https://imdb-api.com/en/API/YouTubeTrailer/k_1cob5uy7/{id_of_film}'
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


print(film('tt1649418'))

# Печать ключей значений из фильма-словаря == y
for key, value in y.items():
    try:
        print(f'{key}  --->  {value}')
    except Exception as e:
        print(f'Oops where have a exception {e}')
        continue

x = {}
for key, value in x.items():
    try:
        if key in ('id', 'fullTitle', 'year', 'image', 'releaseDate', 'runtimeMins', 'plot', 'awards', 'directors',
                   'stars', 'genres', 'companies', 'languages', 'contentRating', 'imDbRating', 'imDbRatingVotes',
                   'metacriticRating', 'trailer', 'boxOffice', 'videoUrl', 'starList'):
            print(f'{key} ---> {value}')
    except Exception as e:
        print(f'Ooops where have exception {e}')
