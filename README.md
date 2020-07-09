# python_from_json
A utility to generate Python model code from a JSON response.

Example usage is shown in `example.py`. It uses an example payload from `https://jsonplaceholder.typicode.com/users`, which currently serves the following response:
```json
[
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  },
  ...
]
```

The response is serialized by the `UnimplementedType.from_json` method and model Python class code for the fields are returned by `UnimplementedType.codegen`, with the response for the above example being:
```python
class User:
	def __init__(self, id=None, name=None, username=None, email=None, address=None, phone=None, website=None, company=None):
		self.id = id
		self.name = name
		self.username = username
		self.email = email
		self.address = address
		self.phone = phone
		self.website = website
		self.company = company

class Address:
	def __init__(self, street=None, suite=None, city=None, zipcode=None, geo=None):
		self.street = street
		self.suite = suite
		self.city = city
		self.zipcode = zipcode
		self.geo = geo

class Geo:
	def __init__(self, lat=None, lng=None):
		self.lat = lat
		self.lng = lng

class Company:
	def __init__(self, name=None, catch_phrase=None, bs=None):
		self.name = name
		self.catch_phrase = catch_phrase
		self.bs = bs
```
