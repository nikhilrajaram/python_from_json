import requests
from UnimplementedType import UnimplementedType

if __name__ == '__main__':
    # using https://jsonplaceholder.typicode.com/users for an example payload
    response = requests.get(url='https://jsonplaceholder.typicode.com/users')
    out = UnimplementedType('user') \
        .unimplementedtype_from_json(response.json()) \
        .codegen(include_nested_classes=True, include_from_json_method=True)

    with open('example/out.py', 'w') as f:
        f.write(out)
