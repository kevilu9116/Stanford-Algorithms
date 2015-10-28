import argparse
import random
import copy
import sys
import math

#test branching

class Graph:
	def __init__(self, graphTxt, delimiter='\t'):
		self.edgesFromNode = {}
		self.edges = []
		self.nodes = []

		for line in graphTxt:
			fields = line.strip().split(delimiter)
			self.edgesFromNode[fields[0]] = fields[1:]
			self.nodes.append(fields[0])
			for i in range(1, len(fields)):
				self.edges.append((fields[0], fields[i])) #edges will be counted twice

	def selectRandomEdge(self):
		return random.choice(self.edges)

	def getNumNodes(self):
		return len(self.nodes)

	def getNumEdges(self):
		return len(self.edges) / 2

	def contractEdge(self, edge):
		node1 = edge[0]
		node2 = edge[1]

		updatedGraph = {}
		newNode = node1 + "-" + node2
		newNodeEdges = []
		newEdgeList = []

		#look at every node connected to node1
		for connectedNode in self.edgesFromNode[node1]:
			"""
			If the connected node is not node1 or node2, we add the connectedNode to the list of connectedNodes for the 
			new, contracted node
			"""
			if connectedNode != node1 and connectedNode != node2: 
				newNodeEdges.append(connectedNode)
				newEdgeList.append((newNode, connectedNode))
		#do node1 procedure for node2
		for connectedNode in self.edgesFromNode[node2]:
			if connectedNode != node1 and connectedNode != node2:
				newNodeEdges.append(connectedNode)
				newEdgeList.append((newNode, connectedNode))

		#now we iterate through every node in the graph (except the two nodes of the given edge)
		for node in self.edgesFromNode:
			if node == node1 or node == node2:
				continue
			updatedGraph[node] = []
			for connectedNode in self.edgesFromNode[node]:
				#if the node used to be connected to node 1 or node2, it is now connected to the contracted node
				if connectedNode == node1 or connectedNode == node2:
					updatedGraph[node].append(newNode)
					newEdgeList.append((node, newNode))
				#else the edge is unchanged
				else:
					updatedGraph[node].append(connectedNode)
					newEdgeList.append((node, connectedNode))

		#add the contracted node to the new graph, and update the graph
		updatedGraph[newNode] = newNodeEdges
		self.edgesFromNode = updatedGraph
		self.edges = newEdgeList

		#update nodes list
		self.nodes.remove(node1)
		self.nodes.remove(node2)
		self.nodes.append(newNode)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", help="Filepath to adjancency list txt file.")
	parser.add_argument("--n", help="Number of iterations done by randomized contraction algorithm.\
	 (Default: (numVertices)^2 * log(numVertices) iterations.", type=int)
	parser.add_argument("--d", help="Delimiter (default '\\t'), type 'space' for ' ' delimiter")
	args = parser.parse_args()

	inputFile = open(args.f, "r")
	if args.d:
		if args.d == 'space':
			originalGraph = Graph(inputFile, ' ')
		else:
			originalGraph = Graph(inputFile, args.d)
	else:
		originalGraph = Graph(inputFile)
	inputFile.close()

	if args.n:
		numRuns = args.n
	else:
		numRuns = int(originalGraph.getNumNodes() * originalGraph.getNumNodes() * math.log(originalGraph.getNumNodes()))

	bestMinCut = sys.maxint
	for i in range(numRuns):
		copyGraph = copy.deepcopy(originalGraph)
		while copyGraph.getNumNodes() > 2:
			randomEdge = copyGraph.selectRandomEdge()
			copyGraph.contractEdge(randomEdge)
		minCut = copyGraph.getNumEdges()
		if minCut < bestMinCut:
			bestMinCut = minCut
	print bestMinCut

if __name__ == '__main__':
	main()

