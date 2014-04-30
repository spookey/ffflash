
from requests import get as rget
from changeffapi import Loader

NODESJSON = 'http://map.freifunk-mainz.de/nodes.json'
FFAPIJSON = 'ffapi_wi.json'

def scrape(url):
    '''returns remote json'''
    try:
        return rget(url).json()
    except Exception as ex:
        print('Error: %s' %(ex))

if __name__ == '__main__':
    nodes = scrape(NODESJSON)

    if nodes:
        online = 0
        loader = Loader(FFAPIJSON)

        for node in nodes['nodes']:
            if node['flags']['online'] and node['name']:
                online += 1

        print('state,nodes => %s\n' %(loader.find(['state', 'nodes'])))

        loader.set(['state', 'nodes'], online)
        print('state,nodes => %s\n' %(loader.find(['state', 'nodes'])))

        loader.dump(overwrite=True)
