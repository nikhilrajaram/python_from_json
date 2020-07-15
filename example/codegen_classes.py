import requests
from UnimplementedType import UnimplementedType

if __name__ == '__main__':
    # using https://pokeapi.co/api/v2/pokemon/ditto for an example payload
    response = requests.get(url='https://pokeapi.co/api/v2/pokemon/ditto')
    out = UnimplementedType('ditto')\
        .serialize_json(response.json())\
        .codegen(include_nested_classes=True, include_from_json_method=True)

    with open('example/out.py', 'w') as f:
        f.write(out)
