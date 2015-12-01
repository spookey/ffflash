
def handle_rankfile(ff, nodelist):
    '''
    Entry function gather results from a retrieved ``--nodelist``  to store it
    into the ``--rankfile``.

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :return: ``True`` if rankfile was modified else ``False``
    '''
    if not ff.access_for('rankfile'):
        return False
    if not nodelist or not isinstance(nodelist, dict):
        return False
