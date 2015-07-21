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

for line in master:
	CMGName = line.split(',',2)[0]
	if CMGName and CMGName != '':
		smiles_param = line.split(',',2)[1]
		cids = pcp.get_cids(smiles_param, 'smiles', searchtype='substructure')
		cas_rns = []
		results = pcp.get_synonyms(cids)
		for result in results:
			for syn in result.get('Synonym', []):
				match = re.match('(\d{2,7}-\d\d-\d)', syn)
	    		if match:
	        		cas_rns.append(match.group(1))
		findings = open('Results/%s.csv'% CMGName, 'a')
		for element in cas_rns:
			findings.write(CMGName + ',' + element + '\n')
		
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



