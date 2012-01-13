import os,urllib
import networkx as nx

BGRID_VERSION = '3.1.84'

def download_zip(ver=BGRID_VERSION):
	"""Download a .zip file from BioGRID
	"""
	os.chdir('data')
	if not os.path.exists(ver):
		os.mkdir(ver)
	os.chdir(ver)
	urllib.urlretrieve('http://thebiogrid.org/downloads/archives/Release%%20Archive/BIOGRID-%s/BIOGRID-ORGANISM-%s.tab2.zip' %(ver,ver),filename='BIOGRID-ORGANISM-%s.tab2.zip' %ver)
	os.chdir('../../')

def download_exists(ver):
	return os.path.exists('data/'+ver)

def getMultiEdges(G,as_Graph=False,minConfirm=2):
	if (type(G) != nx.MultiGraph):
		raise TypeError("need a NetworkX MultiGraph")
	GG = nx.Graph()
	for e in G.edges_iter():
		if (len(G.edge[e[0]][e[1]]) >= minConfirm):
			GG.add_edge(e[0],e[1])
	if as_Graph:
		return GG
	else:
		return GG.edges()

def getSpecies(species,int_type='physical',ver=BGRID_VERSION,id_type='entrez',as_Graph=False,as_MultiGraph=False):
	if not download_exists(ver):
		download_zip(ver)
	os.chdir('data/'+ver+'/')
	if not os.path.exists('BIOGRID-ORGANISM-%s-%s.tab2.txt' %(species,ver)):
		os.system('unzip BIOGRID-ORGANISM-%s.tab2.zip' %ver)
	if not os.path.exists('BIOGRID-ORGANISM-%s-%s.tab2.txt' %(species,ver)):
		raise IOError("Species %s does not exist in BIOGRID-ORGANISM-%s.tab2.zip" %(species,ver))
	os.chdir('../../')
	return getFileNet('data/%s/BIOGRID-ORGANISM-%s-%s.tab2.txt' %(ver,species,ver),int_type=int_type,id_type=id_type,as_Graph=as_Graph,as_MultiGraph=as_MultiGraph)

def getFileNet(fname,int_type='physical',id_type='entrez',as_Graph=False,as_MultiGraph=False):
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
	type_index = header.index('Experimental System Type')
	if as_MultiGraph:
		G = nx.MultiGraph()
	else:
		G = nx.Graph()
	for line in it:
		words = line.rstrip().split('\t')
		if words[type_index]==int_type:
			if words[idA] not in ('',' ','-') and words[idB] not in ('',' ','-') and words[idA]!=words[idB]:
				G.add_edge(words[idA],words[idB])
	if as_Graph:
		return G
	else:
		return G.edges()

def getSpeciesPruned(species,int_type='physical',ver=BGRID_VERSION,id_type='entrez',as_Graph=False,as_MultiGraph=False):
	import networkx as nx
	G = getSpecies(species,ver=ver,int_type=int_type,id_type=id_type,as_Graph=True,as_MultiGraph=as_MultiGraph)
	G = nx.connected_component_subgraphs(G)[0]
	while True:
		bad_nodes = map(lambda (k,v) :k, filter(lambda (k,v) :v<2,G.degree_iter()))
		if len(bad_nodes):
			G.remove_nodes_from(bad_nodes)
		else:
			break
	if as_Graph:
		return G
	else:
		return G.edges()


def getSpeciesPrunedConfirmed(species,int_type='physical',ver=BGRID_VERSION,id_type='entrez',as_Graph=False,minConfirm=2):
	G = getSpeciesPruned(species,int_type=int_type,ver=BGRID_VERSION,id_type='entrez',as_Graph=True,as_MultiGraph=True)
	return getMultiEdges(G,as_Graph=as_Graph,minConfirm=minConfirm)


	








