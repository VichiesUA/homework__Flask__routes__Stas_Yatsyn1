import csv
from random import randint

import requests
from faker import Faker
from flask import Flask

fake = Faker()
app = Flask(__name__)


def create_fake_text():
    # Створюється .тхт файл з рандомним текстом
    with open("random.txt", mode="w") as f:
        f.write(str(fake.text()))


@app.route('/')
def start_page():
    # Стартова сторінка, що б вручну не прописувати шляхи
    return '''
    <h1> ==> <a href = "/requirements"> requirements </a> <br></h1>
    <h1> ==> <a href = "/generate-users"> generate-users </a> <br></h1>
    <h1> ==> <a href = "/space"> space </a></h1>
    <h1> ==> <a href = "/mean"> statistics </a></h1>
    '''


@app.route('/requirements')
def write_file_in_web():
    # Створюється документ з фейк текстом
    create_fake_text()
    # Виводиться цей документ на сторінку
    with open("random.txt", "r") as f:
        return f.read()


@app.route('/generate-users')
def generate_users():
    # Сторінка створення фейкових пошт з рандомною кількістю
    for _ in range(randint(1, 100)):
        yield f'{fake.free_email()} <br>'


@app.route('/generate-users/<count>')
def generate_users1(count):
    # Сторінка створення фейкових пошт (кількість вказать через /)
    for _ in range(int(count)):
        yield f'{fake.free_email()} <br>'


@app.route('/space')
def cosmonauts():
    # В змінну 'r' передаємо дані з сайту
    r = requests.get('http://api.open-notify.org/astros.json', auth=('user', 'pass'))
    # в змінну 'space_engineers_json' передаєм json файл
    space_engineers_json = r.json()
    # count_of_cosmonauts - кількість космонавтів
    count_of_cosmonauts = str(space_engineers_json['number'])
    # message - чи успішна місія
    message = str(space_engineers_json['message'])
    # Багато 'yield'  що б гарно відформатувати вивід
    yield f'Count of cosmonauts ==> {count_of_cosmonauts} <br><br>'
    yield '=======================================================<br>'
    # В циклі берем дані про космонавтів і виводим їх
    for i in space_engineers_json['people']:
        yield f'{i["name"]} crafting ==> {i["craft"]} <br>'
    yield '=======================================================<br><br>'
    yield f'Working ==> {message} <br>'


@app.route('/mean')
def statistics():
    # Функція для обрахунків ваги та зросту
    # змінна для рахування сумми висоти та масси (що б потім можна було знайти середнє арифметичне)
    height_sum = 0
    weight_sum = 0
    # Змінна для обрахунку кількості індексів
    count_of_index = 0
    # Відкриваєм файл та передаємо дані в 'reader_csv'
    with open("people_data.csv", "r") as file_csv:
        reader_csv = csv.DictReader(file_csv)
        # перебираєм стовпчики та отримуєм сумми висоти та ваги і переводим в кг та см і рахуєм кількість людей
        for row in reader_csv:
            height_sum += float(list(row.values())[1]) * 2.54
            weight_sum += float(list(row.values())[2]) * 0.4536
            count_of_index += 1
        # рахуєм середю вагу та висоту
        m_height = height_sum / count_of_index
        m_weight = weight_sum / count_of_index
        # виводим дані на сторінку
        return (
            f"<h1>Середній ріст ==> {round(m_height, 2)} см.</h1><br>"
            f"<h1>Середня вага ==> {round(m_weight, 2)} кг.</h1><br>"
            f"<h1>Кількість людей ==> {count_of_index}</h1><br>"
        )


if __name__ == '__main__':
    app.run()
