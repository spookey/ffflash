
from sys import argv
from datetime import datetime
from requests import get as rget
from changeffapi import Loader

NODESJSON = 'http://map.freifunk-mainz.de/nodes.json'
FFAPIJSON = 'ffapi_file.json'

TWEETRESULT = True

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
        nonclient = 0

        for node in nodes['nodes']:
            if node['flags']['online']:
                online += 1
                if not node['flags']['client']:
                    nonclient += 1

        now = datetime.now().strftime('%H:%M %d.%m.%Y')
        resultmsg = 'Status: online: %d (%d Router, %d Teilnehmer) %s' %(online, nonclient, online-nonclient, now)
        if len(argv) > 1:
            print(resultmsg)
        else:
            loader = Loader(FFAPIJSON)
            if nonclient != int(loader.find(['state', 'nodes'])):
                loader.set(['state', 'nodes'], nonclient)
                loader.dump(overwrite=True)

            if TWEETRESULT:
                from notify.twitter import send_tweet
                send_tweet(resultmsg)
