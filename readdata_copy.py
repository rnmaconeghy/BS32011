#allows my raw dataset to be filtered into  4 different text files that I can use in mySQL to create my tables

#!/usr/bin/python

#reads in the data file GDS4506_full.soft and the command fh - filehandler 
infile='GDS4506_full.soft'

fh = open(infile)

#produces a lost of lines starting at '!dataset_table_begin'
line= fh.readline()
while line[:20] != '!dataset_table_begin':
    line=fh.readline()

header= fh.readline().strip()

#builds a colelction of column names
colnames={}

#spilts the string into a string arrary using /t to seperate them
index=0
for title in header.split('\t'):
    colnames[title]=index
    print '%s\t%s'%(title,index)
    index=index+1



#open our output files, one per table.
genefile=open('genes.txt', 'w')
expressionfile=open('expression.txt','w')
probefile=open('probes.txt', 'w')

#gives names to each column for the output files
genefields=['Gene ID', 'Gene symbol', 'Gene title']
samples=header.split('\t')[2:int(colnames['Gene ID'])-2]
probefields=['ID_REF','Gene ID']

#builds new rows under the columns
def buildrow(row, fields):
    newrow=[]
    for f in fields:
        newrow.append(row[int(colnames[f])])
    return "\t".join(newrow)+"\n"

#builds the rows specifically for the expression file
def build_expression(row, samples):
    exprrows=[]
    for s in samples:
        newrow=[s,]
	newrow.append(row[int(colnames['ID_REF'])])
	newrow.append(row[int(colnames[s])])
	exprrows.append("\t".join(newrow))
    return "\n".join(exprrows)+"\n"
    
#imports data into the files
for line in fh.readlines():
    if line[0]=='!':
       continue
    row=line.strip().split('\t')	
    try:
	genefile.write(buildrow(row, genefields))
    	probefile.write(buildrow(row,probefields))
    	expressionfile.write(build_expression(row,samples))	
    except Exception, e:
        print "Error processing line:\n%s%s"%(line,e)

#closes the new files once the data has been imported
genefile.close()
probefile.close()
expressionfile.close()    
