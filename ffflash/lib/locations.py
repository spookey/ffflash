from os import path

from ffflash.lib.files import check_file_location


def get_basedir():
    '''
    Fancy helper to find project's basedir.
    Use :meth:`locate_file` to reach into the package folder.

    :return: full absolute path to |info_name|\'s basedir
    '''
    return path.abspath(
        path.dirname(path.dirname(path.dirname(__file__)))
    )


def locate_file(*parts, must_exist=False):
    '''
    Find files inside :meth:``get_basedir``.

    :param parts: trail to your file.
        e.g. ``bla/fasel/blubb`` would be ``'bla', 'fasel', 'blubb'``
    :param must_exist: check if located file really exists and is a file
        see :meth:`ffflash.lib.files.check_file_location` for more
    :return: full absolute path to desired file, or ``None`` on error
    '''
    location = path.join(get_basedir(), *parts)
    return check_file_location(location, must_exist=must_exist)
