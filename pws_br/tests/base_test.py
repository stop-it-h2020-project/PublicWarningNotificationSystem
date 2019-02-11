def create_option(name, value, type="string"):
    option = Option()
    option.name = name
    option_values = OptionValues()
    if type == "string":
        option_values.stringValue = value
    if type == "int":
        option_values.intValue = value
    if type == "double":
        option_values.doubleValue = value
    option.values = [option_values]
    return option


class Option(object):
    def __init__(self):
        self.name = ''
        self.values = []


class OptionValues(object):
    def __init__(self):
        self.stringValue = ''
        self.intValue = 0
        self.doubleValue = 0.0


class Point(object):
    def __init__(self):
        self.fieldsDouble = {}
        self.fieldsString = {}
        self.group = ''
        self.time = 0
        self.tags = {}
