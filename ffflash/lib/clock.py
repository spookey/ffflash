from datetime import datetime


def get_iso_timestamp(dt=None):
    '''
    Generate iso timestrings

    :param dt: custom ``datetime`` object, or ``now()`` if ``None``
    :return str: iso representation of ``dt``
    '''
    if not dt:
        dt = datetime.now()
    return dt.isoformat('T')
