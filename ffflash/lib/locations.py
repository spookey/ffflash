from os import path


def get_basedir():
    '''
    Fancy helper to find project's basedir.
    Use :meth:`locate_file` to reach into the package folder.

    :return: full absolute path to |info_name|\'s basedir
    '''
    return path.abspath(
        path.dirname(path.dirname(path.dirname(__file__)))
    )


def check_file_location(location, must_exist=False):
    '''
    Validate path for a file.

    Checks for the parent folder to exist, and that ``location`` itself is
    not a folder.
    Optionally, if ``location`` is an already existing file.

    :param location: path to check
    :param must_exist: check also if ``location`` really exists and is a file
    :return str: validated path of ``location`` if all above conditions
        are met or ``None``
    '''
    location = path.abspath(location)
    parent = path.dirname(location)
    if all([
        path.isdir(parent),
        not path.isdir(location),
        (
            path.exists(location) and path.isfile(location)
        ) if must_exist else True
    ]):
        return location


def check_file_extension(location, *extensions):
    '''
    Validate path for a selection of extensions.

    :param location: path to check
    :param extensions: one or more extensions the ``location`` should end with
    :return tuple: (basename of ``location``, extension of ``location``) or
        (``None``, ``None``) if extension did not match
    '''
    name, extension = path.splitext(path.basename(location))
    if extension and (extension.lower() in [
        ''.join([path.extsep, ext.lstrip(path.extsep).lower()])
        for ext in extensions
    ]):
        return name, extension
    return None, None


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
