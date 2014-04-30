#change ffapi

*replace existing fields in your ffapi.json*


##Usage

    from changeffapi import Loader

    loader = Loader('ffapi.json')

    loader.set(['api'], '1.2.3')
    loader.dump()

You should now have a `ffapi_change.json` file with changed api-string and updated timestring.

* `mapnodes.py` updates current nodes field with json data from [ffmap-d3](https://github.com/ffnord/ffmap-d3)s `nodes.json`
    * requires [python-requests](http://docs.python-requests.org/en/latest) library

