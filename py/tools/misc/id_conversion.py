import re
from string import maketrans


def to_id(text):

    text = re.sub('[^0-9a-zA-Z_]', '', text)
    text = re.sub('^[^a-zA-Z_]+', '', text)

    return text


def xml_to_py(text):

    text = str(text)
    return to_id(text.translate(maketrans('-', '_')))
