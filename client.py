# client.py
import requests
import json

# Базовый URL для API
BASE_URL = "http://127.0.0.1:5000/api"

session = requests.Session()

logged_in_user_id = None

def register_user(first_name, last_name, email, password):
    """Регистрирует нового пользователя через API."""
    print(f"\n--- Регистрация пользователя: {email} ---")
    response = session.post(f"{BASE_URL}/auth/register", json={
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    })
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response

def login_user(email, password):
    """Выполняет вход пользователя через API."""
    global logged_in_user_id
    print(f"\n--- Вход пользователя: {email} ---")
    response = session.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    print(f"Статус: {response.status_code}")
    res_json = {}
    try:
        res_json = response.json()
        print(f"Ответ: {json.dumps(res_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")

    if response.status_code == 200:
        logged_in_user_id = res_json.get('user_id')
        print(f"Успешный вход. ID пользователя (если предоставлен API): {logged_in_user_id}")
    else:
        print("Вход не удался.")
    return response

def logout_user():
    """Выполняет выход пользователя через API."""
    global logged_in_user_id
    print(f"\n--- Выход пользователя ---")
    response = session.post(f"{BASE_URL}/auth/logout")
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    if response.status_code == 200:
        logged_in_user_id = None # Сбросить ID вошедшего пользователя
        print("Пользователь вышел из системы.")
    return response


def get_all_users():
    """Получает список всех пользователей через API."""
    print("\n--- Получение всех пользователей (GET /api/users/) ---")
    response = session.get(f"{BASE_URL}/users/")
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response

def get_user_by_id(user_id):
    """Получает данные пользователя по ID через API."""
    print(f"\n--- Получение пользователя ID {user_id} (GET /api/users/{user_id}/) ---")
    response = session.get(f"{BASE_URL}/users/{user_id}")
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response

def update_user(user_id, first_name=None, last_name=None, email=None, password=None):
    """Обновляет данные пользователя по ID через API (требует аутентификации)."""
    print(f"\n--- Обновление данных пользователя ID {user_id} (PUT /api/users/{user_id}) ---")
    data = {}
    if first_name: data['first_name'] = first_name
    if last_name: data['last_name'] = last_name
    if email: data['email'] = email
    if password: data['password'] = password

    response = session.put(f"{BASE_URL}/users/{user_id}", json=data)
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response

def delete_user(user_id):
    """Удаляет пользователя по ID через API (требует аутентификации)."""
    print(f"\n--- Удаление пользователя ID {user_id} (DELETE /api/users/{user_id}/) ---")
    response = session.delete(f"{BASE_URL}/users/{user_id}")
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response


def create_news(title, content):
    """Создает новую новость через API (требует аутентификации)."""
    print(f"\n--- Создание новости (POST /api/news/) от имени ID {logged_in_user_id} ---")
    response = session.post(f"{BASE_URL}/news/", json={
        "title": title,
        "content": content
    })
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response

def get_all_news():
    """Получает список всех новостей через API."""
    print("\n--- Получение всех новостей (GET /api/news/) ---")
    response = session.get(f"{BASE_URL}/news/")
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response

def update_news(news_id, title=None, content=None):
    """Обновляет существующую новость по ID через API (требует аутентификации и авторства)."""
    print(f"\n--- Обновление новости ID {news_id} (PUT /api/news/{news_id}) ---")
    data = {}
    if title: data['title'] = title
    if content: data['content'] = content

    response = session.put(f"{BASE_URL}/news/{news_id}", json=data)
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response

def delete_news(news_id):
    """Удаляет новость по ID через API (требует аутентификации и авторства)."""
    print(f"\n--- Удаление новости ID {news_id} (DELETE /api/news/{news_id}) ---")
    response = session.delete(f"{BASE_URL}/news/{news_id}/")
    print(f"Статус: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Ответ (не JSON): {response.text}")
    return response


if __name__ == "__main__":
    print("--- Запуск тестового клиента API с аутентификацией Flask-Login ---")

    # 1. Регистрация первого пользователя
    reg_res1 = register_user("Иван", "Иванов", "ivan.ivanov@example.com", "пароль123")
    user1_id_registered = reg_res1.json().get('user_id') if reg_res1.status_code == 201 else None

    # 2. Регистрация второго пользователя
    reg_res2 = register_user("Екатерина", "Петрова", "ekat.petrova@example.com", "секретныйпароль")
    user2_id_registered = reg_res2.json().get('user_id') if reg_res2.status_code == 201 else None

    # 3. Вход первого пользователя
    login_user("ivan.ivanov@example.com", "пароль123")

    # 4. Создание новости от имени первого пользователя
    news_res1 = create_news("Первая новость Ивана", "Контент первой новости, написанной Иваном.")
    news1_id = news_res1.json().get('id') if news_res1.status_code == 201 else None

    news_res2 = create_news("Вторая новость Ивана", "Еще контента от Ивана.")
    news2_id = news_res2.json().get('id') if news_res2.status_code == 201 else None

    # 5. Получение всех новостей (публично)
    get_all_news()

    # 6. Попытка первого пользователя обновить свою новость
    print("\n--- Обновление новости Ивана ---")
    if news1_id:
        update_news(news1_id, title="Обновленная первая новость от Ивана", content="Новый, улучшенный контент от Ивана.")
    else:
        print("ID первой новости не получен, пропускаем обновление.")

    # 7. Попытка первого пользователя обновить профиль второго (должна быть ошибка, если API защищено)
    # Обратите внимание: API обычно позволяет пользователю обновлять только свой профиль.
    print(f"\n--- Попытка Ивана обновить профиль Екатерины (ID: {user2_id_registered}) ---")
    if user2_id_registered:
        # Ожидаемый результат: 403 Forbidden или 401 Unauthorized, если API не разрешает это
        update_user(user2_id_registered, first_name="Екатерина (изменено Иваном - неудачно)")
    else:
        print("ID второго пользователя не получен, пропускаем попытку обновления.")

    # 8. Выход первого пользователя
    logout_user()

    # 9. Вход второго пользователя
    login_user("ekat.petrova@example.com", "секретныйпароль")

    # 10. Создание новости от имени второго пользователя
    news_res3 = create_news("Новость от Екатерины", "Это новость, созданная Екатериной Петровой.")
    news3_id = news_res3.json().get('id') if news_res3.status_code == 201 else None

    # 11. Попытка второго пользователя обновить новость первого (должна быть ошибка)
    print("\n--- Попытка Екатерины обновить новость Ивана (должна быть ошибка) ---")
    if news1_id:
        # Ожидаемый результат: 403 Forbidden, если API разрешает обновление только автору
        update_news(news1_id, title="Новый заголовок от Екатерины (неудачно)")
    else:
        print("ID первой новости не получен, пропускаем попытку обновления.")

    # 12. Второй пользователь удаляет свою новость
    print("\n--- Екатерина удаляет свою новость ---")
    if news3_id:
        delete_news(news3_id)
    else:
        print("ID новости Екатерины не получен, пропускаем удаление.")

    # 13. Выход второго пользователя
    logout_user()

    # 14. Вход Ивана, чтобы удалить свой профиль
    login_user("ivan.ivanov@example.com", "пароль123")
    print(f"\n--- Иван удаляет свой профиль (ID: {logged_in_user_id}) ---")
    if logged_in_user_id:
        delete_user(logged_in_user_id) # + Удаление его новостей
    else:
        print("ID текущего пользователя не получен, пропускаем удаление профиля.")

    # 15. Проверка всех новостей и пользователей после удалений
    get_all_news()
    get_all_users()

    print("\n--- Тестирование API с аутентификацией Flask-Login завершено ---")