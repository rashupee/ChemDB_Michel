""" 
	Early July, 2015. Project with Michel to build csv files with queried data from PubChem using the PubChem
	API wrapper.
	 """

import pubchempy as pcp
import re
import logging

logging.getLogger('pubchempy').setLevel(logging.DEBUG)

# CMGFileName = 'ChemProjTestData.csv'
CMGFileName = 'PracticeData.csv'

master = open(CMGFileName, 'r')

def batchIndexes(cids):
	""" Returns list of indicies to void timeout with pcp.get_synonyms """
	max_batch = 1000
	list_size = len(cids)
	batches = int(len(cids)/max_batch) + 1
	remainder = list_size % max_batch
	begin = 0
	end = 0
	batch_indexes = []
	while index < batches:
		end = begin + max_batch - 1
		batch_indexes.append((begin,end))
		begin = end
		index += 1

	return batch_indexes

for line in master:
	CMGName = line.split(',',2)[0]
	if CMGName and CMGName != '':
		smiles_param = line.split(',',2)[1]
		print "Trying pcp.get_cids method with " + smiles_param + "..."
		try:
			cids = pcp.get_cids(smiles_param, 'smiles', searchtype='substructure')
			batch_indexes = batchIndexes(cids)
			findings = open('Results/%s.csv'% CMGName, 'a')
			for index in batch_indexes:
				cas_rns = []
				print "Processing pcp.get_synonyms with cids batch ", index
				results = pcp.get_synonyms(cids)
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
			print "Checking smiles parameter " + smiles_param + " throws error:"
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



