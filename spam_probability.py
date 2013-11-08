#!/usr/bin/python


import json

json_data = open('spam_dict.txt')
x = json.load(json_data)
json_data.close()

json_data = open('more_spam_dict.txt')
y = json.load(json_data)
json_data.close()

data = dict(x.items()+y.items()) #if same values occur in both, the values of x will be overriden by y value


print 'The size of data dict is {0}'.format(len(data))

"""
its time we calculate the probability of each token. 
As in how much does each token contribute to any spam email

Ham probability = Token frequency in ham messages / Number of ham messages trained on
 
Spam probability = Token frequency in spam messages / Number of spam messages trained on

If either Ham probability or Spam probability are greater than 1.0, set them equal to 1.0.
   
"""

Spam_Token = {}  #stores the contribution of each token to any spam email

for tokens,value in data.iteritems():
	prob = value/1780.0 #tested with 502 emails
	if prob>=1.0:
		prob = 0.999

	Spam_Token[tokens]=prob


for i,j in Spam_Token.iteritems():
	if j>0.2:	
		print i,':',j

with open('spam_token_contribution.db','w') as outfile:
	json.dump(Spam_Token,outfile)
