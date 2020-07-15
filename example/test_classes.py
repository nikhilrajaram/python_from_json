import requests

from example.out import Ditto

if __name__ == '__main__':
    response = requests.get(url='https://pokeapi.co/api/v2/pokemon/ditto')
    print(Ditto.from_json(response.json()).__dict__)
