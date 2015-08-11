""" 
	Early July, 2015. Project with Michel to build csv files with queried data from PubChem using the PubChem
	API wrapper.
	 """

import pubchempy as pcp
import re
import logging

import requests

import time

logging.getLogger('pubchempy').setLevel(logging.DEBUG)

CMGFileName = 'ChemProjTestData.csv'
# CMGFileName = 'PracticeData.csv'

def batchIndexes(cids):
	""" Returns list of indicies to avoid timeout with pcp.get_synonyms """
	max_batch = 1000
	list_size = len(cids)
	batches = int(len(cids)/max_batch) + 1
	remainder = list_size % max_batch
	begin = 0
	end = 0
	batch_indexes = []
	index = 0
	while index < batches:
		end = begin + max_batch - 1
		if end >= list_size - 1:
			batch_indexes.append((begin,list_size - 1))
			break
		batch_indexes.append((begin,end))
		begin = end
		index += 1

	return batch_indexes


""" Build a csv file with CMG names and keys for asynchronous use with PUG REST API """

master = open(CMGFileName, 'r')
keymaster = open('Results/CMGKeyList', 'w')

for line in master:
	CMGName = line.split(',',2)[0]
	smiles_param = line.split(',',2)[1]
	r = requests.get('http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/substructure/smiles/%s/JSON'% smiles_param)
	key = str(r.json()['Waiting']['ListKey'])
	keymaster.write(CMGName + ',' + key + '\n')
	print "Got ket for " + CMGName

keymaster.close()

""" Wait five minutes """
print "Waiting 5 minutes for PubChem to do its thang..."
time.sleep(300)

""" Open keymaster, and work through, line-by-line, matching the CASRNS regex """

for line in keymaster:
	CMGName = line.split(',',2)[0]
	key = line.split(',',2)[1]
	print "Getting cids list for " + CMGName + "..."
	try:
		rr = requests.get('http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/listkey/%s/cids/JSON'% key)
		cids = rr.json()['IdentifierList']['CID']
		""" Split the big list of cids into smaller lists """
		batch_indexes = batchIndexes(cids)
		findings = open('Results/%s.csv'% CMGName, 'a')
		cas_rns = []
		for index in batch_indexes:
			print "Processing pcp.get_synonyms with cids batch ", index
			results = pcp.get_synonyms(cids[index[0]:index[1]])
			print "Finding CASRN matches in the synonyms ..."
			for result in results:
				for syn in result.get('Synonym', []):
					match = re.match('(\d{2,7}-\d\d-\d)', syn)
		    		if match:
		        		cas_rns.append(match.group(1))
		print "Writing results to file ..."
		for element in cas_rns:
			findings.write(CMGName + ',' + element + '\n')
	except Exception as e:
		print "Checking " + CMGName + " throws error:"
		print e.message
		findings = open('Results/%s_error.txt'% CMGName, 'a')
		findings.write(CMGName + ": something is wrong.\nError message is: " + e.message + '\n')

		findings.close()

master.close()








''' Old stuff below '''






# 		try:
# 			print "Checking smiles parameter: " + SmilesParam + " ...."
# 			cids = get_cids(SmilesParam,'smiles', searchtype='substructure'))
# 			print "... seems OK"
# 			CASRN_list = re.findall(r'\d{2,7}-\d\d-\d', nym_string)
# 			findings = open('%s.csv'% Results/CMGName, 'a')
# 			for nym in CASRN_list:
# 				findings.write(CMGName + ',' + nym + '\n')
# 		except Exception as e:
# 			print "Checking smiles parameter " + SmilesParam + " throws error:"
# 			print e.message
# 			findings = open('%s_error.txt'% CMGName, 'a')
# 			findings.write(CMGName + ": something is wrong.\nError message is: " + e.message)
		
# 		findings.close()


# for line in master:
# 	CMGName = line.split(',',2)[0]
# 	if CMGName and CMGName != '':
# 		SmilesParam = line.split(',',2)[1]
# 		try:
# 			nym_string = str(get_synonyms(SmilesParam,'smiles', searchtype='substructure'))
# 			print "Checking smiles parameter " + SmilesParam + ".... seems OK"
# 			CASRN_list = re.findall(r'\d{2,7}-\d\d-\d', nym_string)
# 			findings = open('%s.csv'% CMGName, 'a')
# 			for nym in CASRN_list:
# 				findings.write(CMGName + ',' + nym + '\n')
# 		except Exception as e:
# 			print "Checking smiles parameter " + SmilesParam + " throws error:"
# 			print e.message
# 			findings = open('%s_error.txt'% CMGName, 'a')
# 			findings.write(CMGName + ": something is wrong.\nError message is: " + e.message)
		
# 		findings.close()



# master.close()



