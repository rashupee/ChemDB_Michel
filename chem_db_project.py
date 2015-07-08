""" 
	Early July, 2015. Project with Michel to build csv files with queried data from PubChem using the PubChem
	API wrapper.
	 """

from pubchempy import *
import re

CMGFileName = 'ChemProjTestData.csv'

master = open(CMGFileName, 'r')

for line in master:
	CMGName = line.split(',',2)[0]
	if CMGName and CMGName != '':
		SmilesParam = line.split(',',2)[1]
		try:
			nym_string = str(get_synonyms(SmilesParam,'smiles', searchtype='substructure'))
			CASRN_list = re.findall(r'\d{2,7}-\d\d-\d', nym_string)
			findings = open('%s.csv'% CMGName, 'a')
			for nym in CASRN_list:
				findings.write(CMGName + ',' + nym + '\n')
		except Exception as e:
			findings = open('%s_error.txt'% CMGName, 'a')
			findings.write(CMGName + ": something is wrong.\nError message is: " + e.message)
		
		findings.close()



