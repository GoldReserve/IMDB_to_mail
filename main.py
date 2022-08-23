# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


"""Код ниже отправляет email. Я создал ящик на gmail чтобы отправлять всякое. Мне понадобится отправлять письмо в 
определенном формате чтобы это выглядело классно. Т е постер фильма, каст, актеры и т.п."""
import yagmail

yag = yagmail.SMTP(user='tet.yag2022', password='jmzbgylqzquygkih')
context = ['Привет это 1 тестовое сообщение']
yag.send(to='alamana13@mail.ru', subject='test', contents=context)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
