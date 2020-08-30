# импортируем библиотеку sqlalchemy и некоторые функции из нее
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# импортируем функцию datetime из библиотеки datetime
from datetime import datetime

# импортируем из модуля users класс User
from users import User

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class Athlete(Base):
    """
    Описывает структуру таблицы athelete, хранящую данные об участниках Олимпиады
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # дата рождения атлета
    birthdate = sa.Column(sa.Text)
    # пол атлета
    gender = sa.Column(sa.Text)
    # рост атлета
    height = sa.Column(sa.REAL)
    # имя атлета
    name = sa.Column(sa.Text)
    # вес атлета
    weight = sa.Column(sa.Integer)
    # золотые медали атлета
    gold_medals = sa.Column(sa.Integer)
    # серебряные медали атлета
    silver_medals = sa.Column(sa.Integer)
    # бронзовые медали атлета
    bronze_medals = sa.Column(sa.Integer)
    # общие количество медалей атлета
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна, которую представляет атлет
    country = sa.Column(sa.Text)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def find_user(user_id, session):
    """
    Производит поиск пользователя по заданному id
    """
    # находим запись в таблице User, у которых поле User.id совпадает с параметром user_id
    query = session.query(User).filter(User.id == user_id)
    # составляем список в который передаем дату рождения и рост пользователя
    user_info = [[user.birthdate, user.height] for user in query.all()]
    # возвращаем список с информацией о пользователе
    return user_info


def athlete_filter(session):
    """
    Функция отфильтровывает необходимые данные атлетов
    """
    # отфильтровываем атлетов, у которых заполнен рост
    query = session.query(Athlete).filter(Athlete.height > 0)
    # составляем список в который добавляем имя атлета, дату его рождения и его рост
    athlete_info = [[athlete.name, athlete.birthdate, athlete.height] for athlete in query.all()]
    # возвращаем список с информацией об атлетах
    return athlete_info


def find_athlete(user_info, athlete_info):
    """
    Функция принимает информацию о пользователях и атлетах и выводит на печать совпадения
    """
    # проверяем наличие id, если он есть ищем совпадения, иначе выдаем сообщение, что данного id не существует
    if user_info:
        height_athlete = []
        birthday_athlete = []
        for athlete in athlete_info:
            if athlete[2] == user_info[0][1]:
                height_athlete = athlete
                break
            else:
                diff = abs(user_info[0][1] - athlete[2])
                if not height_athlete:
                    height_athlete = athlete
                else:
                    if abs(user_info[0][1] - height_athlete[2]) > diff:
                        height_athlete = athlete
                    else:
                        continue
        for athlete in athlete_info:
            if athlete[1] == user_info[0][0]:
                birthday_athlete = athlete
                break
            else:
                date_1 = datetime.strptime(user_info[0][0], "%Y-%m-%d")
                date_2 = datetime.strptime(athlete[1], "%Y-%m-%d")
                diff = abs(date_1 - date_2)
                if not birthday_athlete:
                    birthday_athlete = athlete
                else:
                    date_3 = datetime.strptime(birthday_athlete[1], "%Y-%m-%d")
                    if abs(date_1 - date_3) > diff:
                        birthday_athlete = athlete
                    else:
                        continue

        print('Атлет ближайший по росту к данному пользователю:', height_athlete[0], height_athlete[2])
        print('Атлет ближайший по дате рождения', birthday_athlete[0], birthday_athlete[1])

    else:
        print('Данного id не существует')


def main():
    """
    Обрабатывает пользовательский ввод и ищет похожие значения
    """
    print('Модуль производит поиск по id и сравнивает рост и дату рождения пользователя с ростом и датой рождения '
          'атлетов и возращает наиболее близкое значение.  ')
    session = connect_db()
    # просим пользователя ввести id
    user_id = input("Введите id пользователя: ")
    # присваеваем переменным значение созданных функций
    user_info = find_user(user_id, session)
    athlete_info = athlete_filter(session)
    # переменные передаем в функцию find_athlete()
    find_athlete(user_info, athlete_info)


if __name__ == "__main__":
    main()
