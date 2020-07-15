# python_from_json
A utility to generate Python model code from a JSON response.

Example usage is shown in `example/codegen_classes.py`. It uses an example payload from `https://pokeapi.co/api/v2/pokemon/ditto`, which currently serves the following response (ellipses used to truncate long lists):
```json
{
  "abilities": [
    {
      "ability": {
        "name": "limber",
        "url": "https://pokeapi.co/api/v2/ability/7/"
      },
      "is_hidden": false,
      "slot": 1
    },
    ...
  ],
  "base_experience": 101,
  "forms": [
    {
      "name": "ditto",
      "url": "https://pokeapi.co/api/v2/pokemon-form/132/"
    }
  ],
  "game_indices": [
    {
      "game_index": 76,
      "version": {
        "name": "red",
        "url": "https://pokeapi.co/api/v2/version/1/"
      }
    },
    ...
  ],
  "height": 3,
  "held_items": [
    {
      "item": {
        "name": "metal-powder",
        "url": "https://pokeapi.co/api/v2/item/234/"
      },
      "version_details": [
        {
          "rarity": 5,
          "version": {
            "name": "ruby",
            "url": "https://pokeapi.co/api/v2/version/7/"
          }
        },
        ...
      ]
    },
    ...
  ],
  "id": 132,
  "is_default": true,
  "location_area_encounters": "https://pokeapi.co/api/v2/pokemon/132/encounters",
  "moves": [
    {
      "move": {
        "name": "transform",
        "url": "https://pokeapi.co/api/v2/move/144/"
      },
      "version_group_details": [
        {
          "level_learned_at": 1,
          "move_learn_method": {
            "name": "level-up",
            "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
          },
          "version_group": {
            "name": "red-blue",
            "url": "https://pokeapi.co/api/v2/version-group/1/"
          }
        },
        ...
      ]
    }
  ],
  "name": "ditto",
  "order": 203,
  "species": {
    "name": "ditto",
    "url": "https://pokeapi.co/api/v2/pokemon-species/132/"
  },
  "sprites": {
    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/132.png",
    "back_female": null,
    "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/132.png",
    "back_shiny_female": null,
    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png",
    "front_female": null,
    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/132.png",
    "front_shiny_female": null
  },
  "stats": [
    {
      "base_stat": 48,
      "effort": 1,
      "stat": {
        "name": "hp",
        "url": "https://pokeapi.co/api/v2/stat/1/"
      }
    },
    ...
  ],
  "types": [
    {
      "slot": 1,
      "type": {
        "name": "normal",
        "url": "https://pokeapi.co/api/v2/type/1/"
      }
    }
  ],
  "weight": 40
}
```

The response is serialized by the `UnimplementedType.unimplementedtype_from_json` method and model Python class code for the fields are returned by `UnimplementedType.codegen`, which has two optional parameters:
* `include_nested_classes`: when `True`, output will include class code generated for any nested custom objects in the JSON
* `include_from_json_method`: when `True`, generates a `from_json` method for each class, which instantiates and returns an appropriate object given a JSON input

With both these flags set to true, the result of `UnimplementedType.codegen` in `example/codegen_classes.py` is the following (also stored in `examples/out.py`):
```python
class Ditto:
	def __init__(self, abilities=[], base_experience=None, forms=[], game_indices=[], height=None, held_items=[], id=None, is_default=None, location_area_encounters=None, moves=[], name=None, order=None, species=None, sprites=None, stats=[], types=[], weight=None):
		self.abilities = abilities
		self.base_experience = base_experience
		self.forms = forms
		self.game_indices = game_indices
		self.height = height
		self.held_items = held_items
		self.id = id
		self.is_default = is_default
		self.location_area_encounters = location_area_encounters
		self.moves = moves
		self.name = name
		self.order = order
		self.species = species
		self.sprites = sprites
		self.stats = stats
		self.types = types
		self.weight = weight

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Ditto()

		if type(json) is list:
			return [Ditto.from_json(ditto) for ditto in json]

		try:
			abilities = [Abilities.from_json(_abilities) for _abilities in json.get('abilities')]
		except TypeError:
			abilities = []

		try:
			forms = [Forms.from_json(_forms) for _forms in json.get('forms')]
		except TypeError:
			forms = []

		try:
			game_indices = [GameIndices.from_json(_game_indices) for _game_indices in json.get('gameIndices')]
		except TypeError:
			game_indices = []

		try:
			held_items = [HeldItems.from_json(_held_items) for _held_items in json.get('heldItems')]
		except TypeError:
			held_items = []

		try:
			moves = [Moves.from_json(_moves) for _moves in json.get('moves')]
		except TypeError:
			moves = []

		try:
			stats = [Stats.from_json(_stats) for _stats in json.get('stats')]
		except TypeError:
			stats = []

		try:
			types = [Types.from_json(_types) for _types in json.get('types')]
		except TypeError:
			types = []

		return Ditto(abilities, json.get('base_experience'), forms, game_indices, json.get('height'), held_items, json.get('id'), json.get('is_default'), json.get('location_area_encounters'), moves, json.get('name'), json.get('order'), Species.from_json(json.get('species')), Sprites.from_json(json.get('sprites')), stats, types, json.get('weight'))


class Abilities:
	def __init__(self, ability=None, is_hidden=None, slot=None):
		self.ability = ability
		self.is_hidden = is_hidden
		self.slot = slot

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Abilities()

		if type(json) is list:
			return [Abilities.from_json(abilities) for abilities in json]

		return Abilities(Ability.from_json(json.get('ability')), json.get('is_hidden'), json.get('slot'))


class Ability:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Ability()

		if type(json) is list:
			return [Ability.from_json(ability) for ability in json]

		return Ability(json.get('name'), json.get('url'))


class Forms:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Forms()

		if type(json) is list:
			return [Forms.from_json(forms) for forms in json]

		return Forms(json.get('name'), json.get('url'))


class GameIndices:
	def __init__(self, game_index=None, version=None):
		self.game_index = game_index
		self.version = version

	@classmethod
	def from_json(cls, json):
		if json is None:
			return GameIndices()

		if type(json) is list:
			return [GameIndices.from_json(gameIndices) for gameIndices in json]

		return GameIndices(json.get('game_index'), Version.from_json(json.get('version')))


class Version:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Version()

		if type(json) is list:
			return [Version.from_json(version) for version in json]

		return Version(json.get('name'), json.get('url'))


class HeldItems:
	def __init__(self, item=None, version_details=[]):
		self.item = item
		self.version_details = version_details

	@classmethod
	def from_json(cls, json):
		if json is None:
			return HeldItems()

		if type(json) is list:
			return [HeldItems.from_json(heldItems) for heldItems in json]

		try:
			version_details = [VersionDetails.from_json(_version_details) for _version_details in json.get('versionDetails')]
		except TypeError:
			version_details = []

		return HeldItems(Item.from_json(json.get('item')), version_details)


class Item:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Item()

		if type(json) is list:
			return [Item.from_json(item) for item in json]

		return Item(json.get('name'), json.get('url'))


class VersionDetails:
	def __init__(self, rarity=None, version=None):
		self.rarity = rarity
		self.version = version

	@classmethod
	def from_json(cls, json):
		if json is None:
			return VersionDetails()

		if type(json) is list:
			return [VersionDetails.from_json(versionDetails) for versionDetails in json]

		return VersionDetails(json.get('rarity'), Version.from_json(json.get('version')))


class Moves:
	def __init__(self, move=None, version_group_details=[]):
		self.move = move
		self.version_group_details = version_group_details

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Moves()

		if type(json) is list:
			return [Moves.from_json(moves) for moves in json]

		try:
			version_group_details = [VersionGroupDetails.from_json(_version_group_details) for _version_group_details in json.get('versionGroupDetails')]
		except TypeError:
			version_group_details = []

		return Moves(Move.from_json(json.get('move')), version_group_details)


class Move:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Move()

		if type(json) is list:
			return [Move.from_json(move) for move in json]

		return Move(json.get('name'), json.get('url'))


class VersionGroupDetails:
	def __init__(self, level_learned_at=None, move_learn_method=None, version_group=None):
		self.level_learned_at = level_learned_at
		self.move_learn_method = move_learn_method
		self.version_group = version_group

	@classmethod
	def from_json(cls, json):
		if json is None:
			return VersionGroupDetails()

		if type(json) is list:
			return [VersionGroupDetails.from_json(versionGroupDetails) for versionGroupDetails in json]

		return VersionGroupDetails(json.get('level_learned_at'), MoveLearnMethod.from_json(json.get('moveLearnMethod')), VersionGroup.from_json(json.get('versionGroup')))


class MoveLearnMethod:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return MoveLearnMethod()

		if type(json) is list:
			return [MoveLearnMethod.from_json(moveLearnMethod) for moveLearnMethod in json]

		return MoveLearnMethod(json.get('name'), json.get('url'))


class VersionGroup:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return VersionGroup()

		if type(json) is list:
			return [VersionGroup.from_json(versionGroup) for versionGroup in json]

		return VersionGroup(json.get('name'), json.get('url'))


class Species:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Species()

		if type(json) is list:
			return [Species.from_json(species) for species in json]

		return Species(json.get('name'), json.get('url'))


class Sprites:
	def __init__(self, back_default=None, back_female=None, back_shiny=None, back_shiny_female=None, front_default=None, front_female=None, front_shiny=None, front_shiny_female=None):
		self.back_default = back_default
		self.back_female = back_female
		self.back_shiny = back_shiny
		self.back_shiny_female = back_shiny_female
		self.front_default = front_default
		self.front_female = front_female
		self.front_shiny = front_shiny
		self.front_shiny_female = front_shiny_female

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Sprites()

		if type(json) is list:
			return [Sprites.from_json(sprites) for sprites in json]

		return Sprites(json.get('back_default'), json.get('back_female'), json.get('back_shiny'), json.get('back_shiny_female'), json.get('front_default'), json.get('front_female'), json.get('front_shiny'), json.get('front_shiny_female'))


class Stats:
	def __init__(self, base_stat=None, effort=None, stat=None):
		self.base_stat = base_stat
		self.effort = effort
		self.stat = stat

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Stats()

		if type(json) is list:
			return [Stats.from_json(stats) for stats in json]

		return Stats(json.get('base_stat'), json.get('effort'), Stat.from_json(json.get('stat')))


class Stat:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Stat()

		if type(json) is list:
			return [Stat.from_json(stat) for stat in json]

		return Stat(json.get('name'), json.get('url'))


class Types:
	def __init__(self, slot=None, type=None):
		self.slot = slot
		self.type = type

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Types()

		if type(json) is list:
			return [Types.from_json(types) for types in json]

		return Types(json.get('slot'), Type.from_json(json.get('type')))


class Type:
	def __init__(self, name=None, url=None):
		self.name = name
		self.url = url

	@classmethod
	def from_json(cls, json):
		if json is None:
			return Type()

		if type(json) is list:
			return [Type.from_json(type) for type in json]

		return Type(json.get('name'), json.get('url'))


```

One can now easily serialize responses from `https://pokeapi.co/api/v2/pokemon/ditto`, as is seen in `examples/test_classes.py`, by calling the `examples.out.Ditto.from_json` method.
