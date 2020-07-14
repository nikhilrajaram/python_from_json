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


