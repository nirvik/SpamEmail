#!/usr/bin/python

import json

json_data = open('ham_dict.txt')
data= json.load(json_data)
json_data.close()


Ham_Token = {}

for tokens,value in data.iteritems():
	prob = value/2500.0
	if prob>=1.0:
		prob = 0.999
	
	Ham_Token[tokens] = prob


for i,j in Ham_Token.iteritems():
	if j>0.2:
		print i,':',j

with open('ham_token_contribution.db','w') as outfile:
	json.dump(Ham_Token,outfile)

