USERS = [
    {
        "login": "admin",
        "password": "admin",
        "role": "Администратор",
        "full_name": "Администратор Системы",
        "locked": False,
        "attempts": 0,
    },
    {
        "login": "ivanov",
        "password": "1234",
        "role": "Пользователь",
        "full_name": "Иванов Иван",
        "locked": True,
        "attempts": 3,
    },
    {
        "login": "petrov",
        "password": "qwerty",
        "role": "Пользователь",
        "full_name": "Петров Пётр",
        "locked": False,
        "attempts": 0,
    },
]


def all_users():
    return USERS


def find_user(login, password):
    for user in USERS:
        if user["login"] == login and user["password"] == password:
            return user
    return None


def user_by_login(login):
    for user in USERS:
        if user["login"] == login:
            return user
    return None


def login_exists(login):
    for user in USERS:
        if user["login"] == login:
            return True
    return False


def add_user(login, password, role, full_name):
    USERS.append(
        {
            "login": login,
            "password": password,
            "role": role,
            "full_name": full_name,
            "locked": False,
            "attempts": 0,
        }
    )


def update_user(login, password, role, full_name):
    user = user_by_login(login)
    if user is None:
        return False
    user["password"] = password
    user["role"] = role
    user["full_name"] = full_name
    return True


def delete_user(login):
    user = user_by_login(login)
    if user is None:
        return False
    USERS.remove(user)
    return True


def register_fail(login):
    for user in USERS:
        if user["login"] == login:
            user["attempts"] = user["attempts"] + 1
            if user["attempts"] >= 3:
                user["locked"] = True
                return True
            return False
    return False


def reset_attempts(login):
    for user in USERS:
        if user["login"] == login:
            user["attempts"] = 0
            return True
    return False


def unlock_user(login):
    for user in USERS:
        if user["login"] == login:
            user["locked"] = False
            user["attempts"] = 0
            return True
    return False