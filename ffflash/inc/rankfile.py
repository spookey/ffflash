from ffflash.lib.files import check_file_location


def handle_rankfile(ff, nodelist):
    if not ff.access_for('rankfile'):
        return False

    rankfile = check_file_location(ff.args.rankfile, must_exist=False)

    ff.log('{} = {}'.format(ff.args.rankfile, rankfile))
