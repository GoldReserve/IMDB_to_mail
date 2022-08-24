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
    return json_object['items']


def popular():
    y = request()
    count = 1
    for i in range(1, len(y)):
        if isfloat(y[i]['imDbRating']):
            try:
                if float(y[i]['imDbRating']) > 5.5 and int(y[i]['imDbRatingCount']) > 50000 and int(
                        y[i]['year']) > 2018:
                    print(f'№{count}')
                    for key, value in y[i].items():
                        if key not in ['id', 'rankUpDown', 'rank', 'title']:
                            print(f'{key} ---> {value}')
                    print()
                    count += 1
            except Exception as e:
                print(f"something went wrong! ---> {e} ")
                time.sleep(5)
                continue
        else:
            continue


# API key k_1cob5uy7


"""Код ниже отправляет email. Я создал ящик на gmail чтобы отправлять всякое. Мне понадобится отправлять письмо в 
определенном формате чтобы это выглядело классно. Т е постер фильма, каст, актеры и т.п."""

# yag = yagmail.SMTP(user='tet.yag2022', password='jmzbgylqzquygkih')
# context = ['Привет это 1 тестовое сообщение']
# yag.send(to='alamana13@mail.ru', subject='test', contents=context)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    popular()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
