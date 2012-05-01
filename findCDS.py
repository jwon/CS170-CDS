"""
(author: Raf 4/18/2012)
Simple verifyier for the connected dominating set problem.
For more help on NetworkX, start here:
  http://networkx.lanl.gov/tutorial/tutorial.html
"""

import sys
sys.path.append("/home/ff/cs170/project-2012/lib/python2.7/site-packages/")
#print sys.path
from networkx import *


# read example in as an adjacency list
# watch out for trailing whitespace!
G=read_adjlist(path="hw13_5.adjlist",delimiter=" ",nodetype=int)

# print out the graph
print 'adjacency list of the input is:'
print G.adjacency_list()

# draw the graph
# import matplotlib.pyplot as plt
# draw_spring(G)
# plt.show()

# INITIALIZATION START
print "Begin initialization"
if number_connected_components(G) > 1:
    print "DISCONNECTED GRAPH! # of connected components is: ", number_connected_components(G)
    exit()

T = []

for v in G.nodes():
    if G.degree(v) == 1:
        T.append(v)
    if G.degree(v) == (G.number_of_nodes() - 1):
        T = [v]
        break

M = []

for v in T:
    M.extend(G.neighbors(v))

p0 = [T,[], M]

S = [p0]

G1 = minimum_spanning_tree(G)
bestSoFar = G1.nodes()

for v in G.nodes():
    if G.degree(v) == 1:
        bestSoFar.remove(v)

print "Initialization done."

# INITIALIZATION END

def choose(setOfProblems):
    print 'Choose'
    temp = []
    for problem in setOfProblems:
        temp.append(len(problem[1]))

    print "temp: ", temp

    return setOfProblems[temp.index(max(temp))]

def expand(subproblem):
    print 'Expand'
    temp = []
    for m in subproblem[2]:
        newC = list(set(subproblem[0]) | set([m]))
        newN = [x for x in G.neighbors(m) if x not in subproblem[0]]
        newM = []
        for v in newC:
            newM.extend(G.neighbors(v))
        if newN:
            temp.append([newC, newN, newM])
    
    return temp

def lowerBound(subproblem):
    print 'lowerBound'
    tempV = [x for x in G.nodes() if x not in subproblem[0]].sort()
    
    CEdges = set([])

    for v in subproblem[0]:
        CEdges = CEdges | set(G.edges(v))

    tempE = [x for x in G.edges() if x not in list(CEdges)]

    minimum = 0
    limit = 0

    tempGraph = Graph()
    tempGraph.add_nodes_from(tempV)
    tempGraph.add_edges_from(tempE)

    components = number_connected_components(tempGraph)

    while (limit < len(tempGraph.nodes())-components):
        h = 0
        highestDegreeV = null
        for v in tempGraph.nodes():
            if tempGraph.degree(v) > h:
                h = tempGraph.degree(v)
                highestDegreeV = v

        tempGraph.remove_node(highestDegreeV)

        limit += h
        minimum += 1

    return minimum




while S: #while S is not empty
    P_i = choose(S)
    Z = expand(P_i)

    for subproblem in Z:
        if (len(node_boundary(G,subproblem[0]))+len(subproblem[0]) == G.number_of_nodes()) and is_connected(G.subgraph(subproblem[0])):
            bestSoFar = subproblem[0]
        elif lowerBound(subproblem) < len(bestSoFar):
            S.add(subproblem)


print "time to write answer"
f = open('my_answer.txt', 'w')
f.write(bestSoFar)
f.close()


print "DONE!"
