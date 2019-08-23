"""
Common string transformation functions for use with the BaseStringTransformer class.
Note: Uses local import to reduce unneccessary imports.
"""

def normalize(value):
    """
    Normalizes accented characters in a string.

    Parameters
    ----------
    value : str
        The string to sanitize.

    Returns
    -------
    str
        String value with accented characters normalized.
    """
    import unicodedata
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode()

def strip_punctuation(value, replace=""):
    """
    Removes punctuation from a string value.
​
    Parameters
    ----------
    value : str
        The string to remove punctuation from.
​
    Returns
    -------
    str
        String value with punctuation removed.
    """
    import string
    return ''.join(c if c not in string.punctuation else replace for c in value)

def multi_replace(value, mapping=None):
    """
    Replaces characters in a string using a mapping dict.
​
    Parameters
    ----------
    value : str
        String value to replace characters in.
    mapping : dict
        Dict containing search : replace pairs.
​
    Returns
    -------
    str
        String with characters replaced.
    """
    for search, replace in mapping.items():
        value = value.replace(search, replace)
    return value

def hash_string(value, algorithm="sha1"):
    """
    Hashes a string value given the specified algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hashing algorithm.

    Returns
    -------
    str
        Hashed version of the string.
    """
    import hashlib
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Algorith {algorithm} is not available on this system.")

    hash_func = getattr(hashlib, algorithm)
    hash_value = hash_func(value.encode())
    return hash_value.hexdigest()

def split_camel(value):
    """
    Splits CamelCase strings into words.

    Parameters
    ----------
    value : str
        The string to sanitize.

    Returns
    -------
    str
        String as snake_case.
    """
    import re
    return re.sub(r"([a-z0-9]+)([A-Z]{1})", r"\1 \2", value)

def snake_case(value):
    """
    Turns string into snake_case.

    Parameters
    ----------
    value : str
        The string to sanitize.

    Returns
    -------
    str
        String as snake_case.
    """
    return value.lower().replace(" ", "_")
