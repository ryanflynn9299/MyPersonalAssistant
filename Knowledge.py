'''
Ryan Flynn
January 2018
Mr. Maki
Advanced Computer Science
Personal Assistant: Madaket
v3.6
'''

from oauth2client.service_account import ServiceAccountCredentials
import wolframalpha, wikipedia, tweepy, gspread
import re, httplib2, urllib, requests
from random import choice

s_client = None

def ask(q):
    '''
        Ask the Knowledge engine. Get answers from:
        Gspread (custom user input/output)
        Wolfram Alpha API
        Wikipedia API
    '''
    global s_client

    if not q:
        return "Sorry, I didn't get that."
    # Google sheets support
    # Configure table
    try:
        _config_spread()

        table1 = s_client.open('madaket_data').sheet1
        
        # Find any rows with tailored q in cell 1, output cell 2
        pattern = re.compile("['?!,.\"]")
        search = table1.findall(pattern.sub('', q.lower()))
        # print(search)

        if search:
            # print('1')
            res = table1.cell(search[0].row, 2).value
            # print(res)
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
                elif type(ret) == str:
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
                    
                    pat = re.compile('(?<={}).*$'.format(txt))
                    var = pat.search(query).group()
                    ret = table2.cell(table2.find(txt).row, 2).value
                    try:
                        return eval(ret)
                    except NameError:
                        return ret, var
                except Exception:
                    return 'Oops'
    except httplib2.ServerNotFoundError:
        return "Gspread offline"
    
    # Twitter support: posts on twitter according to regex search of query. Does not allow duplicates

    # Wolfram Alpha API: answers query using the Computational Knowledge engine utilized in this API
    try:
        # Attempt setting up the API
        app_id = 'L96JHW-WUHKT49E78'

        client = wolframalpha.Client(app_id)
    except Exception as e:
        
        return "Wolfram Configuration Error"

    try:
        # Query the API
        result = client.query(q)
        answer = next(result.results).text

        return answer
    except urllib.error.URLError:
        return "Wolfram offline"
        try:
            return wikipedia.summary(q, sentences = 2)
        except requests.exceptions.ConnectionError:
            return 'Wikipedia offline'
    except Exception:
        try:
            # print('2')
            # Wikipedia API: answers query if Wolfram Alpha cannot provide an answer.
            return wikipedia.summary(q, sentences = 2)

        except requests.exceptions.ConnectionError:
            return 'Wikipedia offline'
        
        except Exception as e:
            # print('two ',e)
            # If Wikipedia does not have an answer, default to I don't understand string
            return "I don't know that." + "/n" + "You can ask me 'help' to see a list of things I can do."

def learn(question, answer):
    '''
    Teach the Knowledge Engine!
    Customize input and output.
    '''
    
    # Set up
    try:
        _config_spread()
    except httplib2.ServerNotFoundError:
        # Wifi needed
        return "Unable to connect to Gspread"
    
    patt = re.compile("['?!,.\"]")
    question = patt.sub('', question.lower())
    answer = [answer]

    table1 = s_client.open('madaket_data').sheet1

    if question in table1.col_values(1):
        # Adding another response to a learned skill
        try:
            rw = table1.find(question).row
            lst = eval(table1.cell(rw, 2).value)
            # print(lst)
            if type(lst) != list: raise TypeError
            
            if answer[0] not in lst:
                # Add reply to response list and update the table
                lst += answer
                val = str(lst)
                table1.update_cell(rw, 2, val)
                return 'Learned!'
            else:
                return "I already know that."
        except TypeError:
            # To prevent overwriting functions etc
            return 'I can\'t do that at this time.'
        except Exception:
            # General error handling
            return 'Oops!'
    else:
        try:
            # Add input output pair via creating new row
            table1.append_row([question, str(answer)])
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
  
