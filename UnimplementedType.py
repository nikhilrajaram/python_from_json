from UnknownType import UnknownType
import re


class UnimplementedType:
    CLASS_HEADER = "class {}:\n"
    CLASS_INIT = "\tdef __init__(self, {}):\n{}"
    CLASS_PARAMETER = "{}={}"
    CLASS_ASSIGNMENT = "\t\tself.{} = {}"
    CLASS_TERMINATOR = "\n\n"

    def __init__(self, classname, style='underscore'):
        """
        :param classname: name of unimplemented class
        :param style: 'underscore' or 'camelcase' formatting for field names
        """
        self.nested_classes = {}
        self.classname = classname
        self.implementation = ""
        self.style = style

    def from_json(self, json):
        """
        Serialize JSON into UnimplementedType
        :param json: dict-like JSON object
        :return: UnimplementedType object containing schema information from JSON input
        """
        is_list = type(json) is list
        if is_list:
            json = json[0]

        for field, obj in json.items():
            dtype = type(obj)
            if dtype is dict:
                dtype = UnimplementedType(field, style=self.style)\
                    .from_json(obj) if obj != {} else UnknownType()
            if dtype is list:
                dtype = [UnimplementedType(field, style=self.style)
                         .from_json(obj[0])] if len(obj) > 0 else [UnknownType()]
            self.nested_classes[field] = dtype
        return [self] if is_list else self

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
    def codegen_nested_classes(classes, implementations=None):
        """
        Traverse through nested class UnimplementedType representations and codegen each
        For use in UnimplementedType.codegen when include_nested_classes is True
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

            implementations[fieldname] = dtype.codegen(include_nested_classes=False)
            UnimplementedType.codegen_nested_classes(dtype.nested_classes, implementations)

        return list(implementations.values())

    def codegen(self, include_nested_classes=False):
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
        self.implementation += UnimplementedType.CLASS_TERMINATOR

        if not include_nested_classes:
            return self.implementation

        return self.implementation + \
            ''.join([impl for impl in UnimplementedType.codegen_nested_classes(self.nested_classes)])
