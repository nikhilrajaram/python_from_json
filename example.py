import requests
from UnimplementedType import UnimplementedType

if __name__ == '__main__':
    # using https://jsonplaceholder.typicode.com/users for an example payload
    response = requests.get(url='https://jsonplaceholder.typicode.com/users')
    print(UnimplementedType('payload')
          .from_json(response.json())
          .codegen(include_nested_classes=True))
