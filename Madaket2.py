'''
Ryan Flynn
January 2018
Mr. Maki
Advanced Computer Science
Personal Assistant: Madaket
Python 2.7
v2.0
'''

import wolframalpha, wikipedia


while True:
    input = raw_input('How can I help you?/n')
    try:
        app_id = 'L96JHW-WUHKT49E78'

        client = wolframalpha.Client(app_id)

        result = client.query(input)
        answer = next(result.results).text

        print answer
    except Exception as e:
        print e
        print wikipedia.summary(input, sentences = 2)
