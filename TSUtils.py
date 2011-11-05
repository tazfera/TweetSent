#!/usr/bin/python
# -*- coding: utf-8 -*-

import twitter
import re
import uuid
import sys
import urllib

CONSUMERKEY = 'k7ombMSVd3aH6m3F6xjyeAXXXXXX'
CONSUMERSECRET = 'fpRtr508EzI23lrhu6Ybxu69FbHkmWokxLuXN0xY'
ACCESSTOKEN = '391582793-XRRRmcwwpU8aqIVQpvQ9CzpjX9wxWoF5zFmZwl9v'
ACCESSTOKENSECRET = 'hkmRefahe0WX1g3H7i9jmcriIaznzDjuormGhvNDCRo'
TUSER = 't_sent_anal'

DATAPATH = '/Users/taz/Documents/Projects/TweetSentiment/data'

class TSUtils:
    def __init__(self):
        print

    def __del__(self):
        del self

    def search(self, term, page):
        api = twitter.Api(consumer_key=CONSUMERKEY,consumer_secret=CONSUMERSECRET, access_token_key=ACCESSTOKEN, access_token_secret=ACCESSTOKENSECRET, input_encoding='utf-8')
        results = api.GetSearch(term=term, since_id=None, per_page=50, page=page, lang='en', show_user='false', query_users=False)
        rets=[]
        for ret in results:
            if (ret):
                text = ret.text
                text = re.sub(r'RT \@(.*): ', '', text)
                text = re.sub(r'\@([^\s]*)\s', '', text)
                text = re.sub(r'^[^\:]*\:\s', '', text)
                text = re.sub(r'&quot;','"', text)
                text = re.sub(r'&amp;', '&', text)
                text = re.sub(r'&lt;', '<', text)
                text = re.sub(r'&gt;', '>', text)
                text = re.sub(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]', '', text)
                rets.append(text)
        return rets


def tweet_file_classification(tweet, ctype):
    if (ctype == 'positive'):
        type = 'pos'
    elif (ctype == 'negative'):
        type = 'neg'
    elif (ctype == 'neutral'):
        type = 'neu'
    else:
        type = 'ign'

    filename = DATAPATH + '/' + type + '/' + str(uuid.uuid4()) + '.txt'
    print "saving file: ", filename
    f = open(filename,"w") 
    f.write(tweet.encode('utf-8'))
    f.close() 
