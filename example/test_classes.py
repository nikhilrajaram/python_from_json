import requests

from example.out import User

if __name__ == '__main__':
    response = requests.get(url='https://jsonplaceholder.typicode.com/users')
    print(User.from_json(response.json()))
