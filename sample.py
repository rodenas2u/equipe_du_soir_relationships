import networkx as nx
import matplotlib.pyplot as plt
G=nx.karate_club_graph()
print("Node Degree")
nx.draw(G)
plt.show()