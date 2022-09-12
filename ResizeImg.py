import os
import PIL
from PIL import Image
import requests
import shutil


class ResizeImg:
    @staticmethod
    def resize_complete(url: str) -> None:
        """
        :param url: Ссылка на картинку любого формата
        :return: Ничего, но создает файл resized_poster.jpg из исходного файла в рабочей директории.
        """
        r = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open("poster.png", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
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

ResizeImg.resize_complete('')


