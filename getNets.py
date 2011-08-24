
def download_zip(ver='3.1.79'):
	"""Download a .zip file from BioGRID
	download_zip(ver='3.1.79')
	"""
	os.chdir('data')
	if not os.path.exists(ver):
		os.mkdir(ver)
	os.chdir(ver)
	urllib.urlretrieve('http://thebiogrid.org/downloads/archives/Release%20Archive/BIOGRID-3.1.79/BIOGRID-ORGANISM-%s.tab2.zip' %ver)
	os.chdir('../../')

def getSpecies(species,int_type='physical',ver='3.1.79'):
	if not download_exists(ver):
		download_zip(ver)
	os.chdir('data/'+ver+'/')
	if not os.path.exists('BIOGRID-ORGANISM-%s-%s.tab2.txt' %(species,ver)):
		os.system('unzip BIOGRID-ORGANISM-%s.tab2.zip' %ver)
	if not os.path.exists('BIOGRID-ORGANISM-%s-%s.tab2.txt' %(species,ver)):
		raise IOError("Species %s does not exist in BIOGRID-ORGANISM-%s.tab2.zip" %ver)

def getFileNet(fname,int_type='physical',id_type='entrez')
	if int_type not in ('physical','genetic'):
		raise ValueError("interaction types have to be physical or genetic")
	if id_type not in ('entrez','official'):
		raise ValueError("interaction types have to be physical or genetic")
	import networkx as nx
	








