# python_from_json
A utility to generate Python model code from a JSON response.

Example usage is shown in `example/codegen_classes.py`. It uses an example payload from `https://jsonplaceholder.typicode.com/users`, which currently serves the following response:
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

The response is serialized by the `UnimplementedType.unimplementedtype_from_json` method and model Python class code for the fields are returned by `UnimplementedType.codegen`, which has two optional parameters:
* `include_nested_classes`: when `True`, output will include class code generated for any nested custom objects in the JSON
* `include_from_json_method`: when `True`, generates a `from_json` method for each class, which instantiates and returns an appropriate object given a JSON input

With both these flags set to true, the result of `UnimplementedType.codegen` in `example/codegen_classes.py` is the following (also stored in `examples/out.py`):
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

	@classmethod
	def from_json(cls, json):
		if json is None:
			return User()

		if type(json) is list:
			return [User.from_json(user) for user in json]

		return User(json.get('id'), json.get('name'), json.get('username'), json.get('email'), Address.from_json(json.get('address')), json.get('phone'), json.get('website'), Company.from_json(json.get('company')))


class Address:
	def __init__(self, street=None, suite=None, city=None, zipcode=None, geo=None):
		self.street = street
		self.suite = suite
		self.city = city
		self.zipcode = zipcode
		self.geo = geo

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Address()

		if type(json) is list:
			return [Address.from_json(address) for address in json]

		return Address(json.get('street'), json.get('suite'), json.get('city'), json.get('zipcode'), Geo.from_json(json.get('geo')))


class Geo:
	def __init__(self, lat=None, lng=None):
		self.lat = lat
		self.lng = lng

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Geo()

		if type(json) is list:
			return [Geo.from_json(geo) for geo in json]

		return Geo(json.get('lat'), json.get('lng'))


class Company:
	def __init__(self, name=None, catch_phrase=None, bs=None):
		self.name = name
		self.catch_phrase = catch_phrase
		self.bs = bs

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Company()

		if type(json) is list:
			return [Company.from_json(company) for company in json]

		return Company(json.get('name'), json.get('catchPhrase'), json.get('bs'))



```

One can now easily serialize responses from `https://jsonplaceholder.typicode.com/users`, as is seen in `examples/test_classes.py`, by calling the `examples.out.User.from_json` method.
