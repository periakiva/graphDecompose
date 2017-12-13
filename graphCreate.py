import os
from collections import Counter
import plotly.plotly as py
from plotly.graph_objs import *
import networkx as nx
import pickle as p
import matplotlib.pyplot as plt

pathNodes="/home/native/projects/graphDecompose/can_citations.txt"
pathTest="/home/native/projects/graphDecompose/testGraph.txt"

def pickleGraph(path):
    G= nx.read_edgelist(path)
    nx.write_gpickle(G,"graph.gpickle")

#pickleGraph(pathNodes)

def loadGraphPickle():
        return nx.read_gpickle("graph.gpickle")

G = loadGraphPickle()
G.remove_edges_from(G.selfloop_edges())
Gk = nx.k_core(G)
nScc = nx.number_connected_components(G)
coreN = nx.core_number(G)
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
#plotDegreeHist(G)
#degreeSeq = sorted(nx.degree(G).values(),reverse=True)
#print degreeSeq
#print len(G)
#print len(Gk)
print "NUmber of connected components in biggest core: " + str(nScc)
#print coreN.values()
#print type(nScc)
#nodePerCore=Counter(coreN.values())
print "Total Node: " + str(G.number_of_nodes())
print "Total Edges: " + str(G.number_of_edges())

def findVerticesEdges(G):
    vePerCore={}
    SccPerCore={}
    for i in xrange(1,18):
        Gtemp = nx.k_core(G,k=i)
        vePerCore[i]=(Gtemp.number_of_nodes(),Gtemp.number_of_edges())
        SccPerCore[i]=(i,nx.number_connected_components(Gtemp))
    return vePerCore, SccPerCore

vePerCore,SccPerCore = findVerticesEdges(G)

def writeCoresNodes(nodePerCoreDict,SccPerCore):
    with open('nodePerCore.txt','w') as f:
        f.write(str(nodePerCoreDict))
    with open('SccPerCore.txt','w') as f:
        f.write(str(SccPerCore))

writeCoresNodes(vePerCore,SccPerCore)

