'''
Ryan Flynn
January 2018
Mr. Maki
Advanced Computer Science
Personal Assistant: Madaket
v2.4
'''

from nltk import word_tokenize
import wolframalpha, wikipedia,tweepy
import re

def ask(q):
    _tokens = word_tokenize(q)
    if "twitter" in q.lower() or "tweet" in q.lower():
        for phrase in ['post on twitter that','tweet that ', 'post on twitter that ',
                       'post to twitter that','tweet ', 'post to twitter ','post on twitter ']:
            if q.lower().startswith(phrase):
                pat = re.compile('(?<={}).*$'.format(phrase), re.I)
                tweet = pat.search(q).group()
                ret = _tweet(tweet)
                return "Posted!" if not ret else ret
    try:
        app_id = 'L96JHW-WUHKT49E78'

        client = wolframalpha.Client(app_id)
    except Exception as e:
        return "ConfigError"

    try:
        result = client.query(q)
        answer = next(result.results).text

        return answer
    except Exception as e:
        try:
            return wikipedia.summary(q, sentences = 2)
        except Exception:
            return "I don't know that"
def _tweet(text):
    # Fill in the values noted in previous step here
    cfg = { 
        "consumer_key"        : "RtwyVaVoaM7Pr9oIfGXb4Srfo",
        "consumer_secret"     : "7PDuYwkKfGGQQqcevrhmOGE0TSQTsMxd7Z971UN7e0MJpDPikD",
        "access_token"        : "961020047077642241-wbR2RRjDNOVLYL0woWKiHiiXAe1Oqe4",
        "access_token_secret" : "y6tpvGFg3O0Iixhdq4LuSRBQoxgPrPjBU7RsdjYqth9Cq" 
        }

    api = _get_api(cfg)
    try:
        status = api.update_status(text)
        return ''
    except tweepy.error.TweepError:
        return "You already posted that"

def _get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)
  

'''idea: AI: what should I do instead? database? dictionary? nltk for "normalizing" text'''
