import requests

logged_in = False
cookie = None


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


def login(cookie, logged_in):
    auth_data = {
        "username": input('Username: '),
        "password": input('Password: ')
        }

    if not logged_in:
        response = requests.post('http://127.0.0.1:8000/auth/login', json=auth_data)
        if 'Set-Cookie' in response.headers:
            cookie = response.headers['Set-Cookie']
    else:
        response = requests.post('http://127.0.0.1:8000/auth/login', json=auth_data, cookies=cookie)

    json_printer(response.json())

    return cookie


def logout(cookie):
    if cookie is not None:
        response = requests.get('http://127.0.0.1:8000/auth/logout', cookies=cookie)
    else:
        response = requests.get('http://127.0.0.1:8000/auth/logout')

    json_printer(response.json())


def user_info(cookie):
    if cookie is not None:
        response = requests.get('http://127.0.0.1:8000/market/user_info', cookies=cookie)
    else:
        response = requests.get('http://127.0.0.1:8000/market/user_info')

    json_printer(response.json())


def items(cookie):
    if cookie is not None:
        response = requests.get('http://127.0.0.1:8000/market/', cookies=cookie)
    else:
        response = requests.get('http://127.0.0.1:8000/market/')

    json_printer(response.json())


def buy_item(cookie):
    item = input('Item: ')

    if cookie is not None:
        response = requests.get('http://127.0.0.1:8000/market/buy/{}'.format(item), cookies=cookie)
    else:
        response = requests.get('http://127.0.0.1:8000/market/buy/{}'.format(item))

    json_printer(response.json())


def sell_item(cookie):
    item = input('Item: ')

    if cookie is not None:
        response = requests.get('http://127.0.0.1:8000/market/sell/{}'.format(item), cookies=cookie)
    else:
        response = requests.get('http://127.0.0.1:8000/market/sell/{}'.format(item))

    json_printer(response.json())


while True:
    print('\nCommands:', 'register', 'login', 'info', 'items',
          'buy_item', 'sell_item', 'logout', 'exit', sep='\n')

    client_command = input('\n')

    if client_command == 'register':
        register()
    elif client_command == 'login':
        if logged_in:
            login(cookie, logged_in)
        else:
            cookie = login(None, logged_in)
            if cookie is not None:
                cookie = {'session': cookie.split('=')[1].split(';')[0]}
                logged_in = True
    elif client_command == 'info':
        user_info(cookie)
    elif client_command == 'items':
        items(cookie)
    elif client_command == 'buy_item':
        buy_item(cookie)
    elif client_command == 'sell_item':
        sell_item(cookie)
    elif client_command == 'logout':
        logout(cookie)
        logged_in = False
        cookie = None
    elif client_command == 'exit':
        exit()
    else:
        print('\nIncorrect command')