import sys


if sys.version_info[0] == 3:
    string_type = str
else:
    string_type = unicode


def to_bytes(text):
    if isinstance(text, string_type):
        text = text.encode('utf-8')
    return text
