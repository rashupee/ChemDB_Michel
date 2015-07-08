""" 
	Early July, 2015. Project with Michel to build csv files with queried data from PubChem using the PubChem
	API wrapper.
	 """

from pubchempy import *
import re

CMGFileName = 'ChemProjTestData.csv'

master = open(CMGFileName, 'r')

for line in master:
	# print line
	# print type(line)
	# print line.split(',',2)
	CMGName = line.split(',',2)[0]
	if CMGName != '':
		SmilesParam = line.split(',',2)[1]
		findings = open('%s.csv'% CMGName, 'a')
		
		nym_string = str(get_synonyms(SmilesParam,'smiles', searchtype='substructure'))
		CASRN_list = re.findall(r'\d{2,7}-\d\d-\d', nym_string)

		for nym in CASRN_list:
			findings.write(CMGName + ',' + nym + '\n')

		findings.close()



