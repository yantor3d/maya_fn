"""Maya Plug functions."""

import six

__all__ = [
    'plug',
]


def plug(*args):
    """Return the plug built up from the given arguments.
    
    Args:
        *args (str | int): Token(s) to build the plug name from.

    Returns:
        str
    """

    parts = []

    for arg in args:
        if isinstance(arg, int):
            parts[-1] = "{}[{}]".format(parts[-1], arg)
        elif isinstance(arg, six.string_types) and len(arg) == 1:
            parts[-1] = "{}{}".format(parts[-1], arg)
        else:
            parts.append(arg)

    return ".".join(parts)
