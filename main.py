import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
import operator
from collections import OrderedDict

G=nx.Graph().to_undirected()
nodes = ["Roux","Cozette","Rouyer","Prugneau","Latour","Galli","Melissande","Micoud","Moatti","Roche","Séverac","Rouet","Le Guen","Pauwels","Appadoo","Favard","Schneider","Bianchi","Bretagne","Riou","Libbra","Roustan","Tarrago","Blanc","Penot","Gazan","Duluc","Lions","Le Roy","Lemoine","Degorre","Marchand","Anigo","Billong","Guirou","Djellit","Bielderman","Dufy"]
labels = {}
weak_edges = []
strong_edges = []
strong_weights = []
groups = [
	["Micoud","Moatti","Roche","Rouet","Séverac"],
	["Le Guen","Bretagne","Bianchi","Schneider","Riou"],
	["Le Guen","Pauwels","Libbra","Appadoo","Favard"],
	["Micoud","Le Guen","Roustan","Appadoo","Tarrago"],
	["Pauwels","Blanc","Favard","Rouet","Roche"],
	["Micoud","Penot","Gazan","Appadoo"],
	["Le Roy","Lions","Bretagne","Bianchi","Duluc"],
	["Appadoo","Degorre","Lemoine","Séverac","Riou"],
	["Micoud","Anigo","Billong","Djellit","Pauwels"],
	["Schneider","Micoud","Guirou","Favard","Marchand"],
	["Le Guen","Bielderman","Libbra","Blanc","Rouet"],
	["Le Guen","Micoud","Roustan","Tarrago","Moatti"],
	["Roche","Séverac","Schneider","Favard","Bianchi"],
	["Le Guen","Bretagne","Gazan","Djellit","Libbra"], 
	["Micoud","Pauwels","Lions","Marchand","Billong"],
	["Micoud","Roustan","Le Guen","Moatti","Bielderman"],
	["Anigo","Rouyer","Blanc","Riou","Cozette"],
	["Le Guen","Rouyer","Degorre","Penot","Séverac"],
	["Micoud","Pauwels","Duluc","Rouet","Schneider"],
	["Roustan","Le Guen","Tarrago","Micoud","Appadoo"],
	["Melissande","Billong","Riou","Cozette","Appadoo","Degorre"],
	["Séverac","Schneider","Roustan","Moatti","Galli"],
	["Séverac","Micoud","Moatti","Appadoo","Blanc"],
	["Micoud","Roustan","Galli","Rouyer","Dufy"],
	["Latour","Duluc","Blanc","Galli","Schneider"],
	["Degorre","Lions","Penot","Roustan","Pauwels"],
	["Galli","Prugneau","Riou","Lions"],
	["Galli","Moatti","Roux","Roustan","Duluc"],
	["Rouyer","Bielderman","Penot","Dufy","Appadoo"],
	["Micoud","Penot","Degorre","Marchand","Blanc"],
	["Séverac","Melissande","Moatti","Blanc","Latour"],
	["Galli","Roux","Roustan","Nigay","Séverac"],
	["Galli","Micoud","Blanc","Schneider","Latour"],
	["Micoud","Appadoo","Dufy","Latour","Blanc"],
	["Roustan","Séverac","Galli","Melissande","Moatti"],
	["Roustan","Roux","Moatti","Galli","Séverac"],
	["Micoud","Rouyer","Marchand","Bielderman","Latour"]
]

def addAllNodes(nodes):
	for node in nodes:
		G.add_node(node)

def edgeInEdges(edge):
	reversedEdge = (edge[1],edge[0])
	if edge in G.edges() or reversedEdge in G.edges():
		return True

def buildGroupLinks(group):
	size = len(group)
	if size == 1:
		return
	else:
		for i in range(1,size):
			if edgeInEdges((group[0],group[i])):
				G[group[0]][group[1]]['weight'] += 1
			else:
				G.add_edge(group[0],group[i],weight=1)
		del group[0]
		buildGroupLinks(group)

def buildAllGroupLink(groups):
	for group in groups:
		buildGroupLinks(group)

def sortEdges(edges):
	for n1,n2 in edges:
		if G[n1][n2]['weight'] >= 2:
			strong_edges.append(G[n1][n2])
		else:
			weak_edges.append(G[n1][n2])

def labelizeEdge():
	for node in G.nodes():
		labels[node] = node

def drawNetwork():
	edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
	
	edge_weight=dict([((u,v,),int(d['weight'])) for u,v,d in G.edges(data=True)])
	for item in nx.get_edge_attributes(G,'weight').items():
		if item[1] > 1:
			strong_edges.append(item[0])
			strong_weights.append(item[1])

	pos = nx.spring_layout(G,k=1,iterations=100)
	#pos = nx.spring_layout(G)

	#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
	nx.draw_networkx_nodes(G,pos,nodelist=labels,node_color='red',node_size=2000)
	#nx.draw_networkx_edges(G,pos,edgelist=weak_edges,alpha=0.5,edge_color=weights, width=5.0, edge_cmap=plt.cm.Blues)
	edges = nx.draw_networkx_edges(G,pos,edgelist=strong_edges,alpha=1,edge_color=strong_weights, width=5.0, edge_cmap=plt.cm.Blues)
	nx.draw_networkx_labels(G,pos,labels,font_size=16)
	plt.axis('off')
	plt.colorbar(edges)
	for non_edge in nx.non_edges(G):
		print(non_edge)
	plt.show()

def buildMatrix(plot=True,half=True):
	d = pd.DataFrame(0, index=nodes, columns=nodes)
	for item in nx.get_edge_attributes(G,'weight').items():
		assos = item[0]
		d[assos[0]][assos[1]] = item[1]
		d[assos[1]][assos[0]] = item[1]

	if half:
		for i in range(0,d.shape[0]):
			for j in range(0,d.shape[0]):
				if i<j:
					d.ix[i,j] = 0
	if plot:
		getBubbleChart(d)
	return d

def getBubbleChart(d):
	def generateX():
		return np.repeat(np.arange(len(d.index.values)),len(d.index.values))

	def generateY():
		return np.tile(np.arange(len(d.index.values)),len(d.index.values))

	fig, ax = plt.subplots()
	plt.subplots_adjust(left=0.25, bottom=0.25)
	l = plt.scatter(generateX(),generateY(),s=d*50)
	basic_sizes = l._sizes
	plt.xticks(np.arange(0, len(d), 1.0),d.index.values,ha='right', rotation=45)
	plt.yticks(np.arange(0, len(d), 1.0),d.index.values)
	
	plt.grid()

	axcolor = 'lightgoldenrodyellow'
	axsize = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
	ssize = Slider(axsize, 'Size', 1, 20, valinit=50)

	def update(val):
	    new_coef = ssize.val/50
	    new_sizes = [x * new_coef for x in basic_sizes]
	    l._sizes = new_sizes
	    fig.canvas.draw_idle()
	ssize.on_changed(update)
	
	plt.show()

def barChartFromDict(dictionnary, with_mean=False, with_median=False, title=None):
	X = np.arange(0,len(dictionnary),1)
	plt.bar(X, dictionnary.values(), align='center', width=0.5)
	plt.xticks(X , dictionnary.keys(),ha='right', rotation=45)
	if title:
		plt.title(title)
	for i,k in enumerate(dictionnary):
		plt.text(int(i) - 0.5, int(dictionnary[k]) + 1,  str(dictionnary[k]), color='red', fontweight='bold')
	if with_mean:
		plt.axhline(sum(dictionnary.values()) / len(dictionnary), color='black', linestyle='dashed', linewidth=2)
	if with_median:
		plt.axvline(int(getMedian(dictionnary))-0.5, color='black', linestyle='dashed', linewidth=2)
	plt.show()

def getMedian(dictionnary):
	count = 0
	index = 0
	edge = sum(dictionnary.values())/2
	for keys,values in dictionnary.items():
		count += values
		index += 1
		if count > edge:
			return index

def displayDegrees():
	degrees = nx.degree(G)
	sdegrees = sorted(list(degrees.items()),key=operator.itemgetter(1),reverse=True)
	barChartFromDict(OrderedDict(sdegrees))

def clustering():
	clust_coefficients = nx.clustering(G)
	print(clust_coefficients)
	graphs = list(nx.connected_component_subgraphs(G))
	main_node = graphs[0]
	bet_cen = nx.betweenness_centrality(main_node)
	eig_cen = nx.eigenvector_centrality(main_node)
	print(main_node)

addAllNodes(nodes)
buildAllGroupLink(groups)
labelizeEdge()
#drawNetwork()
#buildMatrix()
#displayDegrees()
#clustering()
print("---------------------------")
print("Degree centrality (the number of links incident upon a node) => LIKELIHOOD TO CATCH AN INFORMATION")
print(sorted(list(nx.degree_centrality(G).items()),key=operator.itemgetter(1),reverse=True))
print("---------------------------")
print("---------------------------")
print("Betweenness centrality (quantifies the number of times a node acts as a bridge along the shortest path between two other nodes) => CONTROL ON OTHERS")
print(sorted(list(nx.betweenness_centrality(G).items()),key=operator.itemgetter(1),reverse=True))
print("---------------------------")
print("---------------------------")
print("Eigenvector centrality (a measure of the influence of a node in a network)")
print(sorted(list(nx.eigenvector_centrality(G).items()),key=operator.itemgetter(1),reverse=True))
print("---------------------------")
print("---------------------------")
print("Katz centrality (relative influence of a node)")
print(sorted(list(nx.katz_centrality_numpy(G).items()),key=operator.itemgetter(1),reverse=True))
print("---------------------------")


#http://www.cl.cam.ac.uk/~cm542/teaching/2011/stna-pdfs/stna-lecture11.pdf
