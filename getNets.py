
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

def getSpecies(species,int_type='physical',ver='3.1.79',id_type='entrez',as_Graph=False):
	if not download_exists(ver):
		download_zip(ver)
	os.chdir('data/'+ver+'/')
	if not os.path.exists('BIOGRID-ORGANISM-%s-%s.tab2.txt' %(species,ver)):
		os.system('unzip BIOGRID-ORGANISM-%s.tab2.zip' %ver)
	if not os.path.exists('BIOGRID-ORGANISM-%s-%s.tab2.txt' %(species,ver)):
		raise IOError("Species %s does not exist in BIOGRID-ORGANISM-%s.tab2.zip" %ver)
	os.chdir('../../')
	return getFileNet('data/%s/BIOGRID-ORGANISM-%s-%s.tab2.txt' %(ver,species,ver),int_type=int_type,id_type=id_type)

def getFileNet(fname,int_type='physical',id_type='entrez',as_Graph=False)
	if int_type not in ('physical','genetic'):
		raise ValueError("interaction types have to be physical or genetic")
	if id_type not in ('entrez','official'):
		raise ValueError("interaction types have to be physical or genetic")
	id_type = id_type.upper()
	import networkx as nx
	fi = open(fname,'r')
	it = iter(fi)
	header = it.next().lstrip('#').rstrip().split('\t')
	idA = filter(lambda x: id_type in header[x].upper() and 'A' in header[x].upper(),range(len(header)))[0]
	idB = filter(lambda x: id_type in header[x].upper() and 'B' in header[x].upper(),range(len(header)))[0]
	G = nx.Graph()
	for line in it:
		words = line.rstrip().split('\t')
		if words[id_A] not in ('',' ','-') and words[id_B] not in ('',' ','-'):
			G.add_edge(words[id_A],words[id_B])
	if as_Graph:
		return G
	else:
		return G.edges()

def getSpeciesPruned(species,int_type='physical',ver='3.1.79',id_type='entrez',as_Graph=False)
	import networkx as nx
	G = getSpecies(species,ver=ver,int_type=int_type,id_type=id_type,as+Grapjh=True)
	G = nx.connected_component_subgraphs()[0]
	while True:
		bad_nodes = map(lambda k,v :k, filter(lambda k,v:v<2,G.degree()))
		if len(bad_nodes):
			G.remove_nodes_from(bad_nodes)
		else:
			break
	if as_Graph:
		return G
	else:
		return G.edges()

	
		

	








