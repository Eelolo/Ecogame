import requests

logged_in = False
cookies = None


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


def login(cookies, logged_in):
    auth_data = {
        "username": input('Username: '),
        "password": input('Password: ')
        }

    if not logged_in:
        response = requests.post('http://127.0.0.1:8000/auth/login', json=auth_data)
        if 'Set-Cookie' in response.headers:
            cookies = response.headers['Set-Cookie']
    else:
        response = requests.post('http://127.0.0.1:8000/auth/login', json=auth_data, cookies=cookies)

    json_printer(response.json())

    return cookies


while True:
    print('\nCommands:', 'register', sep='\n')

    client_command = input('\n')

    if client_command == 'register':
        register()
    elif client_command == 'login':
        if logged_in:
            login(cookies, logged_in)
        else:
            cookies = login(None, logged_in)
            if cookies is not None:
                cookies = {'session': cookies.split('=')[1].split(';')[0]}
                logged_in = True
    elif client_command == 'exit':
        exit()
    else:
        print('\nIncorrect command')