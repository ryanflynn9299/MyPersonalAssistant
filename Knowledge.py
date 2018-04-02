'''
Ryan Flynn
January 2018
Mr. Maki
Advanced Computer Science
Personal Assistant: Madaket
v3.4
'''

from oauth2client.service_account import ServiceAccountCredentials
import wolframalpha, wikipedia, tweepy, gspread
import re
from random import choice

s_client = None

def ask(q):
    global s_client

    if not q:
        return "Sorry, I didn't get that."
    # Google sheets support
    # Configure table
    _config_spread()

    table1 = s_client.open('madaket_data').sheet1
    # Find any rows with tailored q in cell 1, output cell 2
    pattern = re.compile("['?!,.\"]")
    search = table1.findall(pattern.sub('', q.lower()))

    if search:
        res = table1.cell(search[0].row, 2).value
        try:
            # Error handling with eval() and gspread output type
            ret = eval(str(res))
            # print(type(ret))
            if type(ret) == list:
                # Detect lists from gspread
                # print('here')
                return choice(ret)
            elif hasattr(ret,'__call__'):
                # Detect funtions
                return ret
        except Exception as e:
            # print('this')
            return str(res)

    # For single parameter function calls from query using gspread: sheet2
    # Twitter support included
    table2 = s_client.open('madaket_data').worksheet('Sheet2')
    
    for txt in table2.col_values(1):
        if q.lower().startswith(txt):
            try:
                pattern = re.compile("['?!,.\"]")
                query = pattern.sub('', q.lower())
                
                pat = re.compile('(?<={}).*$'.format(txt), re.I)
                var = pat.search(query).group()
                return eval(table2.cell(table2.find(txt).row, 2).value)
            except Exception as e:
                print(e)
                return 'Oops'
    

    # Twitter support: posts on twitter according to regex search of query. Does not allow duplicates
    '''
    Deprecated:
    if "twitter" in q.lower() or "tweet" in q.lower():
        for phrase in ['post on twitter that','tweet that ', 'post on twitter that ',
                       'post to twitter that','tweet ', 'post to twitter ','post on twitter ']:
            if q.lower().startswith(phrase):
                pat = re.compile('(?<={}).*$'.format(phrase), re.I)
                tweet = pat.search(q).group()
                ret = _tweet(tweet)
                return "Posted!" if not ret else ret'''

    # Wolfram Alpha API: answers query using the Computational Knowledge engine utilized in this API
    try:
        # Attempt setting up the API
        app_id = 'L96JHW-WUHKT49E78'

        client = wolframalpha.Client(app_id)
    except Exception as e:
        return "ConfigError"

    try:
        # Query the API
        result = client.query(q)
        answer = next(result.results).text

        return answer
    except Exception:
        try:
            # Wikipedia API: answers query if Wolfram Alpha cannot provide an answer.
            return wikipedia.summary(q, sentences = 2)
        
        except Exception:
            # If Wikipedia does not have an answer, default to I don't understand string
            return "I don't know that." + "/n" + "You can ask me 'help' to see a list of things I can do."

def learn(question, answer):
    _config_spread()

    table1 = s_client.open('madaket_data').sheet1
    try:
        table1.append_row([question, answer])
        return 'Learned!'
    except Exception:
        return 'Oops!'
    

def _tweet(text):
    # Unique to my user:
    cfg = { 
        "consumer_key"        : "RtwyVaVoaM7Pr9oIfGXb4Srfo",
        "consumer_secret"     : "7PDuYwkKfGGQQqcevrhmOGE0TSQTsMxd7Z971UN7e0MJpDPikD",
        "access_token"        : "961020047077642241-wbR2RRjDNOVLYL0woWKiHiiXAe1Oqe4",
        "access_token_secret" : "y6tpvGFg3O0Iixhdq4LuSRBQoxgPrPjBU7RsdjYqth9Cq" 
        }
    
    api = _get_api(cfg) # Configure Twitter API with tweepy module
    try:
        status = api.update_status(text) # post tweet
        return 'Posted!'
    except tweepy.error.TweepError:
        return "You already posted that" # Tweepy raises an error if a status already exists

def _config_spread():
    # initialize gspread (Google Drive and Google Sheets APIs)
    global s_client
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/ryanflynn/Downloads/madaket_json.json',
                                                             scope)
    s_client = gspread.authorize(creds)

def _get_api(cfg):
    # set up tweepy to access Twitter API
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def _help():
    # A help function. Posts some questions the user can ask
    return  '''Some questions I can answer:

                What's the weather like?
                What's the square root of pi?
                Who is Abraham Lincoln?
                Tweet I got some food!
                Text 123-456-7890 Hey there.'''
  
