'''
Ryan Flynn
January 2018
Mr. Maki
Advanced Computer Science
Personal Assistant: Madaket
v2.0
'''

import wolframalpha, wikipedia


while True:
    inp = input('How can I help you?/n')
    try:
        app_id = 'L96JHW-WUHKT49E78'

        client = wolframalpha.Client(app_id)

        result = client.query(inp)
        answer = next(result.results).text

        print(answer)
    except Exception as e:
        print(e)
        print(wikipedia.summary(inp, sentences = 2))
