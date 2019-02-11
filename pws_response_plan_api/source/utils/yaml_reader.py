import re
import os

import yaml

pattern = re.compile(r'^\<%= ENV\[\'(.*)\'\] %\>(.*)$')
yaml.add_implicit_resolver("!env", pattern)


def variablenv_constructor(loader, node):
    value = loader.construct_scalar(node)
    envVar, remainingPath = pattern.match(value).groups()
    return os.environ[envVar] + remainingPath


yaml.add_constructor('!env', variablenv_constructor)


def read_yaml_config(filename):
    with open(filename, 'r') as f:
        config = yaml.load(f)
    return config
