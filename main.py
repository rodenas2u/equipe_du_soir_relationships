import networkx as nx
import matplotlib.pyplot as plt

G=nx.Graph()
nodes = ["Micoud","Moatti","Roche","Séverac","Rouet","Le Guen","Pauwels","Appadoo","Favard","Schneider","Bianchi","Bretagne","Schneider","Riou","Libbra","Roustan","Tarrago","Blanc","Penot","Gazan","Duluc","Lions","Le Roy","Lemoine","Degorre","Marchand","Anigo","Billong","Guirou","Djellit","Bielderman","Sebaoun"]


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


addAllNodes(nodes)

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
	["Duluc","Sebaoun","Roche","Cozette","Rioud"]

]

buildAllGroupLink(groups)


labels = {}
weak_edges = []
strong_edges = []
strong_weights = []
labelizeEdge()
#sortEdges(G.edges())

#for n1, n2 in G.edges_iter():
#	print(n1+" "+n2+" "+str(G[n1][n2]['weight']))


edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
edge_weight=dict([((u,v,),int(d['weight'])) for u,v,d in G.edges(data=True)])
for item in nx.get_edge_attributes(G,'weight').items():
	if item[1] > 1:
		strong_edges.append(item[0])
		strong_weights.append(item[1])


pos = nx.spring_layout(G,k=1,iterations=100)
#pos = nx.spring_layout(G)

#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
nx.draw_networkx_nodes(G,pos,nodelist=labels,node_color='red',node_size=2000,)
#nx.draw_networkx_edges(G,pos,edgelist=weak_edges,alpha=0.5,edge_color=weights, width=5.0, edge_cmap=plt.cm.Blues)
edges = nx.draw_networkx_edges(G,pos,edgelist=strong_edges,alpha=1,edge_color=strong_weights, width=5.0, edge_cmap=plt.cm.Blues)
nx.draw_networkx_labels(G,pos,labels,font_size=16)
plt.axis('off')
plt.colorbar(edges)
for non_edge in nx.non_edges(G):
	print(non_edge)
plt.show()

