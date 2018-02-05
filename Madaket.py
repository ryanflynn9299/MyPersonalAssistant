'''
Ryan Flynn
January 2018
Mr. Maki
Advanced Computer Science
Personal Assistant: Madaket
v1.0
'''

import wolframalpha

input = raw_input('How can I help you?')
app_id = '7pL-5km-54P-p79'

client = wolframalpha.Client(app_id)

result = client.query(input)
answer = next(res.results).text

print answer
