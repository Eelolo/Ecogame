import requests

is_logged_in = False
session_cookies = None


def json_printer(json):
    for key in json:
        print(key + ':', json[key])


def register():
    register_data = {
        "username": input('Username: '),
        "password": input('Password: ')
        }

    response = requests.post('http://127.0.0.1:8000/auth/register', json=register_data)
    json_printer(response.json())


def login(session_cookies, is_logged_in):
    auth_data = {
        "username": input('Username: '),
        "password": input('Password: ')
        }

    if not is_logged_in:
        response = requests.post('http://127.0.0.1:8000/auth/login', json=auth_data)
        if 'Set-Cookie' in response.headers:
            session_cookies = response.headers['Set-Cookie']
    else:
        response = requests.post('http://127.0.0.1:8000/auth/login', json=auth_data, cookies=session_cookies)

    json_printer(response.json())

    return session_cookies


def logout(session_cookies):
    if session_cookies is not None:
        response = requests.get('http://127.0.0.1:8000/auth/logout', cookies=session_cookies)
    else:
        response = requests.get('http://127.0.0.1:8000/auth/logout')

    json_printer(response.json())


def user_info(session_cookies):
    if session_cookies is not None:
        response = requests.get('http://127.0.0.1:8000/market/user_info', cookies=session_cookies)
    else:
        response = requests.get('http://127.0.0.1:8000/market/user_info')

    json_printer(response.json())


while True:
    print('\nCommands:', 'register', 'login', 'info', 'logout', sep='\n')

    client_command = input('\n')

    if client_command == 'register':
        register()
    elif client_command == 'login':
        if is_logged_in:
            login(session_cookies, is_logged_in)
        else:
            session_cookies = login(None, is_logged_in)
            if session_cookies is not None:
                session_cookies = {'session': session_cookies.split('=')[1].split(';')[0]}
                is_logged_in = True
    elif client_command == 'info':
        user_info(session_cookies)
    elif client_command == 'logout':
        logout(session_cookies)
        is_logged_in = False
        session_cookies = None
    elif client_command == 'exit':
        exit()
    else:
        print('\nIncorrect command')