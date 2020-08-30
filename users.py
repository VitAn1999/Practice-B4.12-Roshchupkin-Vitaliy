# импортируем библиотеку sqlalchemy и некоторые функции из нее
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.REAL)


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


def create_id():
    """
    Функция создающая id для нового пользователя
    """
    # подключаем сессию
    session = connect_db()
    # создаем query объект
    query = session.query(User)
    # создаем список id пользователей
    users_ids = [user.id for user in query.all()]
    # если список пуст присваиваем id = 1, иначе последний id + 1
    if not users_ids:
        new_id = 1
    else:
        new_id = users_ids[-1] + 1
    return new_id


def valid_email(email):
    """
    Функция для проверки корректности введеного email
    """
    my_list = list()
    count = 0
    for i in email:
        if i == '@':
            count += 1
        my_list.append(i)
    if count == 1:
        [name, domain] = email.split('@')
        if '.' in name:
            return False
        if my_list[0] == '@':
            return False
        if my_list[-1] == '@':
            return False
        if '.' in domain:
            return True
        else:
            return False
    else:
        return False


def valid_birthdate(birthdate):
    """
    Поверка корректности ввода даты рождения
    """
    if len(birthdate) != 10:
        return False
    else:
        count = 0
        for i in birthdate:
            if i == '-':
                count += 1
        if count == 2:
            [year, month, day] = birthdate.split('-')
            if (len(year), len(month), len(day)) == (4, 2, 2):
                return True
            else:
                return False
        else:
            return False


def valid_gender(gender):
    """
    Проверка правильности введения пола
    """
    if gender == "1" or gender == "2":
        return True
    else:
        return False


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в объект User
    """
    # выводим приветствие
    print("Здравствуйте! Эта форма ввода для заполнения базы данных!")
    # запрашиваем у пользователя данные
    first_name = input("Введите ваше имя: ").title()
    last_name = input("Введите вашу фамилию: ").title()

    gender = input("Укажите ваш пол. 1 - мужской, 2 - женский: ")
    # проверка правильности введенного пола
    count = 0
    while count == 0:
        if valid_gender(gender):
            count += 1
        else:
            gender = input('Некорректный ввод данных. Укажите ваш пол. 1 - мужской, 2 - женский: ')

    email = input("Укажите адрес своей электронной почты: ")
    # проводим проверку введеного email
    count = 0
    while count == 0:
        if valid_email(email):
            print('Ваш email принят')
            count += 1
        else:
            email = input('email должен содежать знаки "@" и ".". Введите email еще раз: ')

    birthdate = input("Укажите дату вашего рождения в формате yyyy-mm-dd(например 1999-12-31): ")
    # проводим проверку введеной даты рождения
    count = 0
    while count == 0:
        if valid_birthdate(birthdate):
            print('Ваша дата рождения принята')
            count += 1
        else:
            birthdate = input("Некорректные ввод данных. Укажите дату вашего рождения в формате yyyy-mm-dd(например "
                              "1999-12-31): ")

    height = input("Укажите ваш рост в сантиметрах: ")
    height = int(height)/100
    user_id = create_id()
    # создаем нового пользователя
    user = User(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def find_id(name, session):
    """
    Производит поиск id пользователя по заданному имени
    """
    # находим все записи в таблице User, у которых поле User.first_name совпадает с параметром name
    query = session.query(User).filter(User.first_name == name)
    # подсчитываем количество таких записей в таблице с помощью метода .count()
    users_cnt = query.count()
    # составляем словарь идентификаторов всех найденных пользователей
    user_info = [{user.id: [user.first_name, user.last_name]} for user in query.all()]
    # возвращаем количество найденных пользователей и словарь с именем и id
    return users_cnt, user_info


def print_users_list(cnt, user_info):
    """
    Выводит на экран количество найденных пользователей, их имя и идентификатор.
    Если передан пустой список идентификаторов, выводит сообщение о том, что пользователей не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if user_info:
        # если список не пуст, распечатываем количество найденных пользователей
        print("Найдено пользователей: ", cnt)
        # легенду будущей таблицы
        print("Идентификатор : [Имя, Фамилия]")
        # проходимся по каждому идентификатору
        for user_id in user_info:
            # выводим на экран идентификатор и имя с фамилией
            print(user_id)
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Пользователей с таким именем нет.")


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти id пользователя по имени\n2 - ввести данные нового пользователя\n")
    # проверяем режим
    if mode == "1":
        # выбран режим поиска, запускаем его
        name = input("Введи имя пользователя для поиска: ")
        # вызываем функцию поиска по имени
        users_cnt, user_info = find_id(name, session)
        # вызываем функцию печати на экран результатов поиска
        print_users_list(users_cnt, user_info)
    elif mode == "2":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        print("Некорректный режим:(")


if __name__ == "__main__":
    main()
