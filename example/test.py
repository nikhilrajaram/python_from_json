from example.out import User

import requests

if __name__ == '__main__':
    # using https://jsonplaceholder.typicode.com/users for an example payload
    response = requests.get(url='https://jsonplaceholder.typicode.com/users')
    users = User.from_json(response.json())
    print(users)
