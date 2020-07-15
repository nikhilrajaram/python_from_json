from UnknownType import UnknownType
import re


class UnimplementedType:
    CLASS_HEADER = "class {}:\n"
    CLASS_INIT = "\tdef __init__(self, {}):\n{}"
    CLASS_PARAMETER = "{}={}"
    CLASS_ASSIGNMENT = "\t\tself.{} = {}"
    CLASS_TERMINATOR = "\n\n"
    FROM_JSON_INIT = "\t@classmethod\n\tdef from_json(cls, json):\n"
    FROM_JSON_IMPL = "\t\tif json is None:\n\t\t\treturn {}()\n\n\t\tif type(json) is list:\n\t\t\treturn {}\n\n"
    FROM_JSON_LIST = "[{}.from_json({}) for {} in json]"
    FROM_JSON_RETURN = "\t\treturn {}({})"
    FROM_JSON_DICT_GET = "json.get('{}')"
    FROM_JSON_META_CALL = "{}.from_json({})"
    FROM_JSON_TRY_CATCH = "\t\ttry:\n\t\t\t{} = [{} for _{} in {}]\n\t\texcept TypeError:\n\t\t\t{} = []\n\n"

    def __init__(self, classname, style='underscore'):
        """
        :param classname: name of unimplemented class
        :param style: 'underscore' or 'camelcase' formatting for field names
        """
        self.nested_classes = {}
        self.classname = classname
        self.implementation = ""
        self.style = style

    def unimplementedtype_from_json(self, json):
        """
        Serialize JSON into UnimplementedType
        :param json: dict-like JSON object
        :return: UnimplementedType object containing schema information from JSON input
        """
        is_list = type(json) is list
        if is_list:
            json = json[0]

        if type(json) is not dict:
            return type(json)

        for field, obj in json.items():
            dtype = type(obj)
            if dtype is dict:
                dtype = UnimplementedType(field, style=self.style) \
                    .unimplementedtype_from_json(obj) if obj != {} else UnknownType()
            if dtype is list:
                dtype = [UnimplementedType(field, style=self.style)
                         .unimplementedtype_from_json(obj[0])] if len(obj) > 0 else [UnknownType()]
            self.nested_classes[field] = dtype
        return self

    @staticmethod
    def snaked_to_camelcase(s):
        """
        Converts a string separated by underscores to camelCase
        credit: https://stackoverflow.com/questions/4303492/how-can-i-simplify-this-conversion-from-underscore-to-camelcase-in-python
        :param s: input string
        :return: camelCased output
        """
        return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)

    @staticmethod
    def camelcase_to_snaked(s):
        """
        Converts a camelCase string to a string separated by underscores
        credit: https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
        :param s: input string
        :return: underscore separated output
        """
        return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

    @staticmethod
    def capitalize(s):
        """
        Capitalizes a string
        :param s: input string
        :return: capitalized output
        """
        strlen = len(s)
        if strlen <= 0:
            raise ValueError()
        return s[0].upper() if strlen == 1 else s[0].upper() + s[1:]

    @staticmethod
    def lowercase(s):
        """
        Lowercases a string
        :param s: input string
        :return: lowercased output
        """
        strlen = len(s)
        if strlen <= 0:
            raise ValueError()
        return s[0].lower() if strlen == 1 else s[0].lower() + s[1:]

    @staticmethod
    def codegen_nested_classes(classes, implementations=None, include_from_json_method=False):
        """
        Traverse through nested class UnimplementedType representations and codegen each
        For use in UnimplementedType.codegen when include_nested_classes is True
        :param include_from_json_method: whether or not to include from_json method in codgens
        :param classes: nested classes dict
        :param implementations: accumulator dict during traversal
        :return: list of generated class code for all nested classes
        """
        if implementations is None:
            implementations = {}

        for fieldname, dtype in classes.items():
            if type(dtype) is list:
                if len(dtype) > 0:
                    dtype = dtype[0]

            if type(dtype) is not UnimplementedType or fieldname in implementations:
                # type is primitive or has already been recorded
                continue

            implementations[fieldname] = dtype.codegen(include_nested_classes=False,
                                                       include_from_json_method=include_from_json_method)
            UnimplementedType.codegen_nested_classes(dtype.nested_classes, implementations,
                                                     include_from_json_method=include_from_json_method)

        return list(implementations.values())

    @staticmethod
    def codegen_from_json_method(classname, fields):
        """
        Generate code for a custom class's from_json method
        :param classname: custom class classname
        :param fields: tree-like representation of custom class fields; dict with keys: fieldnames and values: datatypes
        :return: implementation for custom class's from_json method
        """
        # start implementation with classmethod annotation, from_json declaration
        implementation = UnimplementedType.FROM_JSON_INIT
        classname_lowercase = UnimplementedType.lowercase(classname)
        # create list comprehension statement, e.g. [User.from_json(user) for user in json]
        list_comprehension_stmt = UnimplementedType.FROM_JSON_LIST.format(classname, classname_lowercase,
                                                                          classname_lowercase)
        # append to implementation null checking and list checking for input json
        #   if json is list, call from_json for each element of json list
        implementation += UnimplementedType.FROM_JSON_IMPL.format(classname, list_comprehension_stmt)

        # list of parameters to pass to base custom class from_json method
        parameters = []

        for fieldname, dtype in fields.items():
            if type(dtype) is UnimplementedType:
                # type is custom, parameter will be of form Class.from_json(json.get('class'))
                field_classname_uppercase = UnimplementedType.capitalize(dtype.classname)
                fieldname_camelcased = UnimplementedType.snaked_to_camelcase(fieldname)
                fieldname_classname = UnimplementedType.capitalize(fieldname_camelcased)

                # create json get statement, e.g. json.get('class')
                json_get_stmt = UnimplementedType.FROM_JSON_DICT_GET.format(fieldname_camelcased)
                # append to parameters custom class from_json call passed the json.get statement
                parameters.append(
                    UnimplementedType.FROM_JSON_META_CALL.format(fieldname_classname, json_get_stmt)
                )
            elif type(dtype) is list:
                if len(dtype) == 0 or type(dtype[0]) is not UnimplementedType:
                    # list is empty/nested type is primitive
                    # no custom class from_json call is necessary, parameter will be of form json.get('class')
                    parameters.append(UnimplementedType.FROM_JSON_DICT_GET.format(fieldname))
                    continue

                # list is not empty and nested type is custom
                fieldname_camelcased = UnimplementedType.snaked_to_camelcase(fieldname)
                fieldname_classname = UnimplementedType.capitalize(fieldname_camelcased)

                # create json get statement, e.g. json.get('class')
                json_get_stmt = UnimplementedType.FROM_JSON_DICT_GET.format(fieldname_camelcased)
                # create custom class from_json statement, e.g. Class.from_json(json.get('class'))
                from_json_stmt = UnimplementedType.FROM_JSON_META_CALL.format(
                    fieldname_classname, '_' + fieldname)
                # add to implementation try-catch clause for creation of a list of custom classes via list comprehension
                implementation += UnimplementedType.FROM_JSON_TRY_CATCH.format(
                    fieldname, from_json_stmt, fieldname, json_get_stmt, fieldname
                )
                parameters.append(fieldname)
            elif type(dtype) is type:
                # type is primitive, no custom class from_json call is necessary, use simple json.get
                parameters.append(UnimplementedType.FROM_JSON_DICT_GET.format(fieldname))

        # add to implementation from_json call for base custom class with parameters joined by commas
        implementation += UnimplementedType.FROM_JSON_RETURN.format(classname, ', '.join(parameters))
        return implementation

    def codegen(self, include_nested_classes=False, include_from_json_method=False):
        """
        Generate code for custom class
        :param include_nested_classes: when True, will generate code for nested custom classes
        :param include_from_json_method: when True, will add from_json methods to generated code
        :return: implementation for custom class
        """
        self.implementation = ""

        # populate list of fieldnames, datatypes, and default constructor parameters
        fieldnames, dtypes, defaults = [], [], []
        for fieldname, dtype in self.nested_classes.items():
            if self.style == 'underscore':
                fieldname = UnimplementedType.camelcase_to_snaked(fieldname)
            else:
                fieldname = UnimplementedType.snaked_to_camelcase(fieldname)
            fieldnames.append(fieldname)
            dtypes.append(dtype)
            defaults.append([] if type(dtype) is list else None)

        classname_uppercase = UnimplementedType.capitalize(self.classname)
        self.classname = UnimplementedType.snaked_to_camelcase(classname_uppercase)
        # add class declaration to implementation
        self.implementation += UnimplementedType.CLASS_HEADER.format(self.classname)
        # create string with parameters for constructor for custom classes
        parameters = ', '.join([UnimplementedType.CLASS_PARAMETER.format(fieldname, default)
                                for fieldname, default in zip(fieldnames, defaults)])
        # create string with constructor assignments
        assignments = '\n'.join([UnimplementedType.CLASS_ASSIGNMENT.format(fieldname, fieldname)
                                 for fieldname in fieldnames])
        # add constructor to implementation
        self.implementation += UnimplementedType.CLASS_INIT.format(parameters, assignments)

        if include_from_json_method:
            self.implementation += '\n\n'
            # add from_json method to implementation
            self.implementation += UnimplementedType.codegen_from_json_method(self.classname, self.nested_classes)

        self.implementation += '\n\n\n'

        if include_nested_classes:
            self.implementation += ''.join([impl for impl in UnimplementedType.codegen_nested_classes(
                self.nested_classes, include_from_json_method=include_from_json_method)])

        return self.implementation
