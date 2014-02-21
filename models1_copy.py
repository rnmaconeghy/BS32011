'''Classes to represent our gene expression objects'''

import MySQLdb

class DBHandler():
    connection=None
    dbname='rnmaconeghy'
    dbuser='rnmaconeghy'
    dbpassword='javawalk'
'''automatically reconnects if the connection breaks'''    
    def __init__(self):
        if DBHandler.connection == None:
            DBHandler.connection = MySQLdb.connect(db=DBHandler.dbname, \
user=DBHandler.dbuser, passwd=DBHandler.dbpassword)
'''creates a cursor to use in python'''
    def cursor(self):
	return DBHandler.connection.cursor()

class Gene():
    '''This is a class that represents a gene and its variables '''
    gene_symbol=''
    gene_title=''
    gene_ID=''
    probelist=[]

 	

    def __init__(self,gene_ID):
	'''Object initialiser. This takes just one argument, gene_ID.'''
	self.gene_ID=12683
	db=DBHandler()
	cursor=db.cursor()
	sql='select gene_title, gene_symbol from Genes where gene_ID=%s'
	cursor.execute(sql,(gene_ID))
	#query database using sql command
	#get result and populate the class fields.
	result=cursor.fetchone()
	self.gene_title	=result[0]
	self.gene_symbol=result[1]
	#now fetch the probes..
	probesql='select ID_REF from Probes where gene_ID=%s'
	cursor.execute(probesql, (self.gene_ID,))
	resultlist=cursor.fetchall()
	for result in cursor.fetchall():
  	    self.probelist.append(result[0])

    def get_expression(self,Experiment):
	'''retrieves a list of all expression values for this gene for 
the specified experiment'''

        exprlist = gene.get_expression('GSM967008')
        db=DBHandler()
        cursor=db.cursor()
	sql='select expression_value from Expressions_2 where probename=%s and experiment=%s'
	exvals=[] 
	for p in self.probelist:
	    try:
	    	cursor.execute(sql,(p, experiment))
	    	exvals.append(cursor.fetchone()[0]) #add the value to the list of values.
	    except Exception, e:
		raise Exception('Error occurred retrieving expression data for probe %s and experiment %s:%s'%(p,experiment,e))
	return exvals
