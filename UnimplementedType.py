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
        strlen = len(s)
        if strlen <= 0:
            raise ValueError()
        return s[0].upper() if strlen == 1 else s[0].upper() + s[1:]

    @staticmethod
    def lowercase(s):
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
    def codegen_from_json_method(classname, classes):
        implementation = UnimplementedType.FROM_JSON_INIT
        lower_classname = UnimplementedType.lowercase(classname)
        list_clause = UnimplementedType.FROM_JSON_LIST.format(classname, lower_classname, lower_classname)
        implementation += UnimplementedType.FROM_JSON_IMPL.format(classname, list_clause)

        parameters = []

        for fieldname, dtype in classes.items():
            if type(dtype) is UnimplementedType:
                upper_classname = UnimplementedType.capitalize(dtype.classname)

                json_get = UnimplementedType.FROM_JSON_DICT_GET.format(UnimplementedType.snaked_to_camelcase(fieldname))
                parameters.append(UnimplementedType.FROM_JSON_META_CALL.format(upper_classname, json_get))
            elif type(dtype) is list:
                if type(dtype[0]) is UnimplementedType:
                    upper_fieldname = UnimplementedType.capitalize(fieldname)
                    json_get = UnimplementedType.FROM_JSON_DICT_GET.format(
                        UnimplementedType.snaked_to_camelcase(fieldname))
                    from_json_call = UnimplementedType.FROM_JSON_META_CALL.format(upper_fieldname, '_' + fieldname)
                    implementation += UnimplementedType.FROM_JSON_TRY_CATCH.format(
                        fieldname, from_json_call, fieldname, json_get, fieldname)
                    parameters.append(fieldname)
                else:
                    parameters.append(UnimplementedType.FROM_JSON_DICT_GET.format(fieldname))
            else:
                parameters.append(UnimplementedType.FROM_JSON_DICT_GET.format(fieldname))

        implementation += UnimplementedType.FROM_JSON_RETURN.format(classname, ', '.join(parameters))
        return implementation

    def codegen(self, include_nested_classes=False, include_from_json_method=False):
        self.implementation = ""
        fieldnames, dtypes, defaults = [], [], []
        for fieldname, dtype in self.nested_classes.items():
            if self.style == 'underscore':
                fieldname = UnimplementedType.camelcase_to_snaked(fieldname)
            else:
                fieldname = UnimplementedType.snaked_to_camelcase(fieldname)
            fieldnames.append(fieldname)
            dtypes.append(dtype)
            defaults.append([] if type(dtype) is list else None)

        self.classname = UnimplementedType.snaked_to_camelcase(self.classname[0].upper() + self.classname[1:])
        self.implementation += UnimplementedType.CLASS_HEADER.format(self.classname)
        parameters = ', '.join([UnimplementedType.CLASS_PARAMETER.format(fieldname, default)
                                for fieldname, default in zip(fieldnames, defaults)])
        assignments = '\n'.join([UnimplementedType.CLASS_ASSIGNMENT.format(fieldname, fieldname)
                                 for fieldname in fieldnames])
        self.implementation += UnimplementedType.CLASS_INIT.format(parameters, assignments)

        if include_from_json_method:
            self.implementation += '\n\n'
            self.implementation += UnimplementedType.codegen_from_json_method(self.classname, self.nested_classes)

        self.implementation += '\n\n\n'

        if not include_nested_classes:
            return self.implementation

        return self.implementation + \
            ''.join([impl for impl in UnimplementedType.codegen_nested_classes(
                self.nested_classes, include_from_json_method=include_from_json_method)])
