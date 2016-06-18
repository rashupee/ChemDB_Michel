# The synonyms will be written to a CMG#####.csv file if the synonym is CASRN


# Open file, take contents into a list object. Then batch indicies on the cids list.
# Use regex to match with CASRN form. Write to target file results three csv columns:
# CMGname,CASRN,IUPACName

# The synonyms will be written to a CMG#####.csv file

import pubchempy as pcp
import re
import requests

def workOnCMG(CMGName):

	source_filename='CIDS_CMG/CIDS_%s.txt' %(CMGName)
	target_filename='CIDS_Results/%s.csv' %(CMGName)

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


	def cidsList(source_filename):
	# Build cids list

		cids=[]
		master=open(source_filename, 'r')
		for line in master:
			cids.append(line.replace('\n',''))
		master.close()
		return cids

	cids=cidsList(source_filename)

	findings = open(target_filename, 'a')

	for index in batchIndexes(len(cids)):
		print "Processing pcp.get_synonyms with cids batch ", index
		results = pcp.get_synonyms(cids[index[0]:index[1]])
		print "Finding CASRN matches in the synonyms ..."
		for result in results:
			for syn in result.get('Synonym', []):
				match = re.match('(\d{2,7}-\d\d-\d)', syn)
				c=pcp.Compound.from_cid(result.get('CID'))
	    		if match and c.iupac_name:
	    			findings.write(CMGName + "," + match.group(1) + "," + c.iupac_name + '\n')
	    		elif match and not c.iupac_name:
	    			findings.write(CMGName + "," + match.group(1) + ",\n")
	    		elif not match and c.iupac_name:
	    			findings.write(CMGName + ",," + c.iupac_name + '\n')
	findings.close()

CMGList=['CMG12823','CMG13562','CMG10005','CMG10007']
for CMGName in CMGList:
	workOnCMG(CMGName)
