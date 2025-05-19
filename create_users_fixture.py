import json
from django.contrib.auth.hashers import make_password
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Настройки
FIXTURE_FILE = 'users/fixtures/users_fixture.json'  # Путь для сохранения
COMMON_PASSWORD = 'tszh12345'  # Пароль для всех пользователей

# Данные пользователей
users_data = [
    # Глава ТСЖ
    {
        "username": "glava1",
        "first_name": "Иван",
        "last_name": "Главный",
        "role": 1,
        "phone": "79010000001",
        "entrance": 1,
        "apartment": 1,
        "floor": 1
    },

    # Члены ТСЖ (2)
    {
        "username": "member1",
        "first_name": "Петр",
        "last_name": "Членов",
        "role": 2,
        "phone": "79020000001",
        "entrance": 1,
        "apartment": 2,
        "floor": 1
    },
    {
        "username": "member2",
        "first_name": "Ольга",
        "last_name": "Членова",
        "role": 2,
        "phone": "79020000002",
        "entrance": 1,
        "apartment": 3,
        "floor": 2
    },

    # Жильцы (3, двое из одной квартиры)
    {
        "username": "zhilec1",
        "first_name": "Анна",
        "last_name": "Жильцова",
        "role": 3,
        "phone": "79030000001",
        "entrance": 1,
        "apartment": 10,
        "floor": 3
    },
    {
        "username": "zhilec2",
        "first_name": "Олег",
        "last_name": "Жильцов",
        "role": 3,
        "phone": "79030000002",
        "entrance": 1,
        "apartment": 10,  # Та же квартира, что у zhilec1
        "floor": 3
    },
    {
        "username": "zhilec3",
        "first_name": "Мария",
        "last_name": "Квартирантова",
        "role": 3,
        "phone": "79030000003",
        "entrance": 1,
        "apartment": 11,
        "floor": 3
    },

    # Специалисты (3)
    {
        "username": "santehnik1",
        "first_name": "Сергей",
        "last_name": "Трубов",
        "role": 4,
        "phone": "79040000001",
        "profession": "Сантехник"
    },
    {
        "username": "electric1",
        "first_name": "Михаил",
        "last_name": "Проводов",
        "role": 4,
        "phone": "79040000002",
        "profession": "Электрик"
    },
    {
        "username": "uborshik1",
        "first_name": "Галина",
        "last_name": "Чистова",
        "role": 4,
        "phone": "79040000003",
        "profession": "Уборщик"
    }
]


def create_fixture():
    hashed_password = make_password(COMMON_PASSWORD)
    fixture = []

    for user in users_data:
        fixture.append({
            "model": "users.customuser",
            "fields": {
                "password": hashed_password,
                "last_login": None,
                "is_superuser": False,
                "username": user["username"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "email": "",
                "is_staff": False,
                "is_active": True,
                "date_joined": now().isoformat(),
                "role": user["role"],
                "phone": user["phone"],
                "avatar": "",
                "entrance": user.get("entrance"),
                "apartment": user.get("apartment"),
                "floor": user.get("floor"),
                "profession": user.get("profession")
            }
        })

    with open(FIXTURE_FILE, 'w', encoding='utf-8') as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)

    print(f"Файл фикстур создан: {FIXTURE_FILE}")
    print(f"Пароль для всех пользователей: {COMMON_PASSWORD}")


if __name__ == "__main__":
    create_fixture()