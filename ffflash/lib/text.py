from re import search, sub


def search_text(rx, text):
    '''
    Safe search ``text`` with regex.

    :param rx: regex to match on ``text``
    :param text: content to work on
    :return: either ``None`` if ``rx`` is not in ``text`` or
        **match-object** of **re**.
    '''
    return (
        None if not (rx and text) else search(rx, text)
    )


def replace_text(rx, replacement, text):
    '''
    Replace text if ``rx`` matches.

    :param rx: regex to match on ``text``
    :param replacement: content to put into ``text`` on ``rx`` match
    :param text: content to work on
    :return str: ``text`` with replaced parts, or unchanged ``text``
    '''
    if (replacement and search_text(rx, text)):
        return sub(rx, replacement, text)
    return text
