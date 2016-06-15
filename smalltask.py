import random

def shorup(fname):
	# To use this function:
	# Create a directory somewhere convenient from the commandline:
	# 	mkdir Project
	#
	# Put the original csv file here with a name like 'prob.csv'
	# Also put the text file smalltask.py in this directory
	#
	# Go into that directory
	#	cd Project
	#
	# 
	#
	#
	#
	#

	filename=fname
	f = open(fname, 'r')
	g = open('unjag.csv', 'w')
	for line in f:
		l=line.split(',')
		count=len(l)
		if count > 1: # Just in case the second field is empty
			c=1
			while c < count:
				gline='%s,%s\n' %(str(l[0]),l[c].replace('"','').replace('\n','').lstrip())
				g.write(gline)
				c+=1
		else:
			g.write(line)
	f.close()
	g.close()


def fake():
	f=open('fake.csv','w')
	i=100
	i_0=0
	while i_0 < i:
		line='%s,%s,%s\n' %(str(random.random()), str(random.random()), str(random.random()))
		f.write(line)
		i_0+=1
	f.close()

def t(fname):
	f=open(fname,'r')
	first=f.readline()
	second=f.readline()
	print first
	print second.replace('"','').replace('\n','')
	f.close()
