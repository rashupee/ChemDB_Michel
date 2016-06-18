# Will add apostrophe to front of CASRN notation in second position of csv file


CMGNameList=['CMG10006.csv',
'CMG10010.csv',
'CMG10017.csv',
'CMG10039.csv',
'CMG10069.csv',
'CMG10513.csv',
'CMG10535.csv',
'CMG12601.csv',
'CMG12602.csv',
'CMG12823.csv',
'CMG13139.csv',
'CMG13154.csv',
'CMG13156.csv',
'CMG14839.csv'
]

masterDir='Results/'
targetDir='ResultsWApos/'

def makeReplacementFile(CMGName):
	masterFile=open(masterDir + CMGName, 'r')
	targetFile=open(targetDir + CMGName, 'a')

	for line in masterFile:
		nline=line.split(',')
		replacement=nline[0] + ",'" +nline[1]
		targetFile.write(replacement)

	masterFile.close()
	targetFile.close()

for CMGName in CMGNameList:
	makeReplacementFile(CMGName)