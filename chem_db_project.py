
# Early July, 2015. Project with Michel to build csv files with queried data from PubChem using the PubChem
# API wrapper.

import pubchempy as pcp
import re
import logging
import requests
import time

logging.getLogger('pubchempy').setLevel(logging.DEBUG)



def batchIndexes(list_size):
	# Returns list of indicies to avoid timeout with pcp.get_synonyms
	batch_size = 300
	batches = int(list_size/batch_size) + 1
	remainder = list_size % batch_size
	begin = 0
	end = 0
	batch_indexes = []
	index = 0
	while index < batches:
		end = begin + batch_size - 1
		if end >= list_size - 1:
			batch_indexes.append((begin,list_size - 1))
			break
		batch_indexes.append((begin,end))
		begin = end
		index += 1
	return batch_indexes

# Build a csv file with CMG names and keys for asynchronous use with PUG REST API

CMGFileName = 'ChemProjTestData.csv'

master = open(CMGFileName, 'r')
keymaster = open('Results/CMGKeyList.csv', 'w')
keyerrors = open('Results/CMGKeyListErrors.csv', 'w')

for line in master:
	CMGName = line.split(',',2)[0]
	if CMGName and CMGName != '':
		smiles_param = line.split(',',2)[1].replace('\n','')
		print "smiles_param is " + smiles_param
		addy = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/substructure/smiles/%s/JSON' % smiles_param
		# substructure is always asynchronous and returns a key
		r = requests.get(addy)
		r_status = r.status_code
		print "status code is ", r_status
		print ""
		print ""
		if r_status != 202:
			keyerrors.write(CMGName + ',' + 'status code=' + str(r_status) + '\n')
		else:
			key = str(r.json()['Waiting']['ListKey'])
			keymaster.write(CMGName + ',' + key + '\n')
keyerrors.close()
keymaster.close()
master.close()


# Hey, wait just a damn minute!
print "Waiting 3 minutes for PubChem to collect its thoughts..."
time.sleep(180)

# Open keymaster, and work through, line-by-line, matching the CASRNS regex
keymaster = open('Results/CMGKeyList.csv', 'r')
for line in keymaster:
	data = line.split(',',2)
	CMGName = data[0]
	key = str(data[1]).replace('\n', '')
	print "Getting cids list for " + CMGName + " with key " + key
	try:
		rr = requests.get('http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/listkey/%s/cids/JSON'% key)
		cids = rr.json()['IdentifierList']['CID']
		# Split the big list of cids into smaller lists
		list_length = len(cids)
		batch_indexes = batchIndexes(list_length)
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

keymaster.close()



# Work on getting lists of cids first.
# keep records on whether getting the list of cids was successful or not - I think this is the pinch point

# For the successful cids lists, just do what is here already. I think it works: pcp.get_synonyms...

# Then retry the unsuccessful 




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



