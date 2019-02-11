import re

from pws_common.enums import ActionFormatEnum

regex_url_valid = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_url_valid(url):
    if not isinstance(url, str):
        return False

    return re.match(regex_url_valid, url) is not None


def is_message_valid(message):
    return isinstance(message, str)


def is_format_valid(format):
    if not isinstance(format, int):
        return False

    if not ActionFormatEnum.has_value(format):
        return False

    return True
