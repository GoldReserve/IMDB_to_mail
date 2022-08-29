import os

import PIL
from PIL import Image
import urllib.request


class ResizeImg:
    @staticmethod
    def my_resize():
        # Мы делаем запрос и сохраняем пикчу
        urllib.request.urlretrieve(
            'https://images.unsplash.com/photo-1543373014-cfe4f4bc1cdf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVu'
            'fDB8fHx8&auto=format&fit=crop&w=1348&q=80', 'poster.png')

        # Открываем картинку
        img = Image.open("poster.png")

        # Метод чтобы открыть её и увидеть
        # img.show()

        # Меняет размер на необходимый
        resized_image = img.resize((320, 320))
        resized_image.save('resized_poster.png')

    @staticmethod
    def resize_complete(url: str) -> None:
        """
        :param url: Ссылка на картинку любого формата
        :return: Ничего, но создает файл resized_poster.jpg из исходного файла в рабочей директории.
        """

        #Делаем запрос и скачивает с url картинку в рабочую директорию
        urllib.request.urlretrieve(
            url, 'poster.png')
        mywidth = 1024
        img = Image.open('poster.png')

        #Дальше мы делаем resize да так чтобы исходное соотношение сторон не менялось.
        wpercent = (mywidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))

        # PIL.Image.Resampling(1) это способ ресемплинга. Меня вполне устраивает 1
        img = img.resize((mywidth, hsize), PIL.Image.Resampling(1))
        img.save('resized_poster.jpg')

        # Удаляем изначально скаченный файл
        os.remove('poster.png')

ResizeImg.resize_complete('https://proxy.imgsmail.ru/?e=1662022091&email=alamana13%40mail.ru&flags=0&h=-9ue7IyCQA-o5jxBUfIzvw&is_https=1&url173=bS5tZWRpYS1hbWF6b24uY29tL2ltYWdlcy9NL01WNUJNelZsTW1ZMk5UY3RPRGd3T0MwME5ETXpMV0V6TVdZdE0yUmlZbUl5TlROaE1USTBYa0V5WGtGcWNHZGVRWFZ5TlRBek56Z3dOVGdALl9WMV9SYXRpbzAuNjc2Ml9BTF8uanBn')


