# -*- coding: utf8 -*-
import sys
import os
from pyramid.paster import bootstrap
from pymongo import MongoClient
import scit.users

db=None

def setup(settings):
    global db
    db=MongoClient(settings['mongo.uri'])[settings['mongo.db']]

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def run(settings):

    scit.users.init_db(db,settings)
    
def main():
    if 2!=len(sys.argv):
        usage(sys.argv)
    env = bootstrap(sys.argv[1])
    settings=env['registry'].settings
    setup(settings)

    run(settings)

if __name__=='__main__':
    main()
