'''
Ryan Flynn
January 2018
Mr. Maki
Advanced Computer Science
Personal Assistant: Madaket
v2.0
'''

import wolframalpha, wikipedia

def ask(q):
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


'''idea: AI: what should I do instead? database? dictionary? nltk for "normalizing" text'''
