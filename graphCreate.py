import os
import plotly.plotly as py
from plotly.graph_objs import *
import networkx as nx
import pickle as p
import matplotlib.pyplot as plt

pathNodes="/home/native/projects/graphDecompose/can_citations.txt"
pathTest="/home/native/projects/graphDecompose/testGraph.txt"

def pickleGraph(path):
    G= nx.read_edgelist(path)
    nx.write_gpickle(G,"graph2.gpickle")

pickleGraph(pathTest)

def loadGraphPickle():
        return nx.read_gpickle("graph2.gpickle")

G = loadGraphPickle()
G.remove_edges_from(G.selfloop_edges())
Gk = nx.k_core(G)
#G=nx.dodecahedral_graph()
def plotGraph(G):
    pos=nx.spring_layout(G)
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    p=nx.single_source_shortest_path_length(G,ncenter)
    nx.draw_networkx_edges(G,pos,nodelist=[ncenter],alpha=0.4)
    nx.draw_networkx_nodes(G,pos,nodelist=p.keys(),node_size=20,node_color=p.values(),cmap=plt.cm.Reds_r)
    #plt.draw()
    plt.xlim(-.05,1.05)
    plt.ylim(-.05,1.05)
    plt.axis('off')
    plt.show()

def plotDegreeHist(G):
    degreeSeq = sorted(nx.degree(G).values(),reverse=True)
    dmax=max(degreeSeq)
    plt.loglog(degreeSeq,'b-',marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")
    Gcc = sorted(nx.connected_component_subgraphs(G),key=len,reverse=True)[0]
    pos = nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc,pos,node_size=20)
    nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
    plt.show()
#plotGraph(G)
plotDegreeHist(G)
#degreeSeq = sorted(nx.degree(G).values(),reverse=True)
#print degreeSeq
#print len(G)
"""
pos = nx.spring_layout(G)
print pos
print G.edges()
edge_trace = Scatter(x=[],y=[],line=Line(width=0.5,color='#888'),hoverinfo='none',mode='lines')

for edge in G.edges():
    x0,y0 = G.node[edge[0]][pos]
    x1,y1 = G.node[edge[1]]['pos']
    edge_trace['x']+=[x0,x1,None]
    edge_trace['y']+=[y0,y1,None]

node_trace=Scatter(x=[],y=[],text=[],mode='markers',hoverinfo='text',marker=Marker(showscale=True,colorscale='YIGnBu',reversescale=True,color=[],size=10,colorbar=dict(thickness=15,title='Node Connections',xanchor='left',titleside='right'),line=dict(width=2)))

for node in G.nodes():
    x,y=G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

for node,adjacencies in enumerate(G.adjacency_list()):
    node_trace['marker']['color'].append(len(adjacencies))
    node_info = '# of connections: ' + str(len(adjacencies))
    node_trace['text'].append(node_info)

fig = Figure(data=Data([edge_trace,node_trace]),layout=Layout(title='<br>Network graph made with Python',titlefont=dict(size=16),showlegend=False,hovermode='closest',margin=dict(b=20,l=5,r=5,t=40),annotations=[ dict(text="bla bla bla",showarrow=False,xref="paper",yref="paper",x=0.005,y=-0.002)],xaxis=XAxis(showgrid=False,zeroline=False,showticklabels=False),yaxis=YAxis(showgrid=False,zeroline=False,showticklabels=False)))

py.iplot(fig,filename='networkx')
"""
