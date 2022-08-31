import os
import PIL
from PIL import Image
import urllib.request


class ResizeImg:
    #Изначальная функция которая делала resize без сохрания соотношения сторон
    @staticmethod
    def my_resize() -> None:
        # Мы делаем запрос и сохраняем пикчу
        urllib.request.urlretrieve(
            'https://images.unsplash.com/photo-1543373014-cfe4f4bc1cdf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVu'
            'fDB8fHx8&auto=format&fit=crop&w=1348&q=80', 'poster.png')

        # Открываем картинку
        img = Image.open("poster.png")

        # Метод, чтобы открыть её и увидеть
        img.show()

        # Меняет размер на необходимый
        resized_image = img.resize((320, 320))
        resized_image.save('resized_poster.png')

    @staticmethod
    def resize_complete(url: str) -> None:
        """
        :param url: Ссылка на картинку любого формата
        :return: Ничего, но создает файл resized_poster.jpg из исходного файла в рабочей директории.
        """

        # Делаем запрос и скачивает с url картинку в рабочую директорию
        urllib.request.urlretrieve(
            url, 'poster.png')
        mywidth = 1024
        img = Image.open('poster.png')

        # Дальше мы делаем resize да так, чтобы исходное соотношение сторон не менялось.
        wpercent = (mywidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))

        # PIL.Image.Resampling(1) это способ ресемплинга. Меня вполне устраивает 1
        img = img.resize((mywidth, hsize), PIL.Image.Resampling(1))
        img.save('resized_poster.jpg')

        # Удаляем изначально скаченный файл
        os.remove('poster.png')
