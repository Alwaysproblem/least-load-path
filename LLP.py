#!/usr/bin/python3
# least load Path based using Dijkstra algorithm
# the test envirnment :
# Python 3.6.3 (default, Oct  3 2017, 21:45:48)
# [GCC 7.2.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# writen by Prophet 22/10/2017 16:02


class Graph(object):
    def __init__(self, graph):
        self.adjacentlist = {}
        self.nV = 0
        self.nE = 0
        self.graph = graph.lstrip('\n')
        self.ref = list()
        self.make_ref()
        self.insertEdges()
        self.total_num()

    def make_ref(self):
        """
        text process -- change the text format into adjacent list graph.
        """
        self.ref = self.graph.split('\n')
        if self.ref[-1] == '':
            self.ref.pop()
        self.ref = [i.split() for i in self.ref]

        def int_str(x):
            if x.isdigit():
                return int(x)
            else:
                return x

        self.ref = [list(map(int_str, i)) for i in self.ref]


    def insertEdge(self, edge):
        """
        insertEdge into adjacent list graph.
        """
        if edge[0] in self.adjacentlist.keys():
            if tuple(edge[1:]) not in self.adjacentlist[edge[0]]:
                self.adjacentlist[edge[0]].append(tuple(edge[1:]))
            else:
                pass
        else:
            self.adjacentlist[edge[0]] = [tuple(edge[1:])]

    def insertEdges(self):
        """
        insertEdge into adjacent list bidirection graph.
        """
        for i in self.ref:
            self.insertEdge(i)
            k = [i[1], i[0]] + i[2:]
            self.insertEdge(k)
            self.nE += 2


    def removeEdge(self, edge):
        # edge = list(map(int_str, edge_str))
        if edge[0] in self.adjacentlist.keys():
            while tuple(edge[1:]) in self.adjacentlist[edge[0]]:
                self.adjacentlist[edge[0]].remove(tuple(edge[1:]))
            return tuple(edge[1:]) not in self.adjacentlist[edge[0]]
        else:
            return False

    def total_num(self):
        self.nV = len(self.adjacentlist)

    def graph_print(self):
        print("this is the Graph:")
        print(f"the number of vertices is {self.nV}")
        print(f"the number of edges is {self.nE}:")
        for i in self.adjacentlist.keys():
            print("{} : {}".format(i, self.adjacentlist[i]))


def relax_along_LLP(cur_node, next_node, weight, dist, prev, comp):
    """
    the relax-along algorithm of finding least load Path using Dijkstra
    """
    cur_node = ord(cur_node) - ord('A')
    next_node = ord(next_node) - ord('A')

    comp[cur_node] = dist[cur_node]
    if weight > comp[cur_node]:
        comp[cur_node] = weight
    alt = comp[cur_node]
    if alt < dist[next_node]:
        dist[next_node] = alt
        prev[next_node] = cur_node

def LLP_SM(graph, src):
    # initialize all the parameter
    inf = 1/0.000000000000000001
    visited = set(graph.adjacentlist.keys())
    comp = [ 0 for _ in range(graph.nV)]
    dist = [ inf for _ in range(graph.nV)]
    prev = [ -1 for _ in range(graph.nV)]
    dist[ord(src) - ord('A')] = 0

    while(len(visited) != 0):
        mini_dist = min([dist[ord(s) - ord('A')] for s in visited])
        for s in visited:
            if dist[ord(s) - ord('A')] == mini_dist:
                min_s = s

        for i in graph.adjacentlist[min_s]:
            weight = i[1]
            relax_along_LLP(min_s, i[0], weight, dist, prev, comp)

        visited.remove(min_s)
    return src, dist, prev


def show_path(src, dest, dist, prev):
    path = [dest]
    tmp = dest
    print("the maximum load on this path to {} is {}.".format(dest, dist[ord(dest) - ord("A")]))
    while tmp != src or tmp == -1:
        tmp = prev[ord(tmp) - ord('A')] + ord('A')
        tmp = chr(tmp)
        path.append(tmp)
    path.reverse()
    print("the least load path to {} is {}.".format(dest, path))
    return path


graph = \
"""
A B 14
A C 9
A D 7
B E 5
C B 4
C F 3
D C 10
D F 15
F E 8
"""
g = Graph(graph)
g.graph_print()  # that is the undirected graph.

src, dist, prev = LLP_SM(g,'A')
x = list(range(len(prev)))
x = [i for i in x if i != ord(src) - ord('A')]

for i in x:
    show_path(src, chr(i + ord('A')), dist, prev)
