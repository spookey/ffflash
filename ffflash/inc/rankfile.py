
def handle_rankfile(ff, nodelist):
    if not ff.access_for('rankfile'):
        return False
    if not nodelist or not isinstance(nodelist, dict):
        return False
