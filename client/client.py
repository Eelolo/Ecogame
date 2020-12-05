import requests


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


while True:
    print('\nCommands:', 'register', sep='\n')

    client_command = input('\n')

    if client_command == 'register':
        register()
    elif client_command == 'exit':
        exit()
    else:
        print('\nIncorrect command')