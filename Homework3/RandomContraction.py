import argparse
import random
import copy
import sys
import math

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
				if (fields[i], fields[0]) not in self.edges:
					self.edges.append((fields[0], fields[i]))

	def selectRandomEdge(self):
		return random.choice(self.edges)

	def getNumNodes(self):
		return len(self.nodes)

	def getNumEdges(self):
		return len(self.edges)

	def contractEdge(self, edge):
		node1 = edge[0]
		node2 = edge[1]

		# print "Edge selected: " + node1 + "\t" + node2
		# print "Edge dict before contraction: " + str(self.edgesFromNode)
		# print "Edges before contraction: " + str(self.edges)
		# print "Nodes before contraction: " + str(self.nodes)

		#Remove node1 and node2 from nodes list, add new contracted node to nodes list
		self.nodes.remove(node1) 
		self.nodes.remove(node2)
		newNode = node1 + "-" + node2
		self.nodes.append(newNode)
		newNodeEdges = []

		for connectedNode in self.edgesFromNode[node1]: #look at all nodes connected to node1
			if connectedNode != node2: #if the node is not the other half of the random edge
				newNodeEdges.append(connectedNode) #add this node to the nodes connected to the new contracted node
				self.edgesFromNode[connectedNode].remove(node1) #remove the reference from connectedNode to node 1 (as node 1 will be deleted)
				#remove the edge from the edge list (as it's being contracted)
				if (connectedNode, node1) in self.edges:
					self.edges.remove((connectedNode, node1)) 
				elif (node1, connectedNode) in self.edges:
					self.edges.remove((node1, connectedNode))
				self.edgesFromNode[connectedNode].append(newNode) #add the new contracted node to the list of nodes connected to 'connectedNode'
				self.edges.append((connectedNode, newNode)) #add this new edge to the edge list

			#Otherwise, we remove any self-edges formed as a result of the contraction
			#from the edge list.
			else:
				if (node1, node2) in self.edges:
					self.edges.remove((node1, node2))
				elif (node2, node1) in self.edges:
					self.edges.remove((node2, node1))

		
		#Repeat subprocess done for node1 for node 2
		for connectedNode in self.edgesFromNode[node2]:
			if connectedNode != node1:
				newNodeEdges.append(connectedNode)
				self.edgesFromNode[connectedNode].remove(node2)
				if (connectedNode, node2) in self.edges:
					self.edges.remove((connectedNode, node2))
				elif (node2, connectedNode) in self.edges:
					self.edges.remove((node2, connectedNode))
				self.edgesFromNode[connectedNode].append(newNode)
				self.edges.append((connectedNode, newNode))
			else:
				if (node1, node2) in self.edges:
					self.edges.remove((node1, node2))
				elif (node2, node1) in self.edges:
					self.edges.remove((node2, node1))

		#finally, we add the newNode to our edgesFromNode dict and remove both key references to the old, uncontracted nodes
		self.edgesFromNode[newNode] = newNodeEdges
		self.edgesFromNode.pop(node1)
		self.edgesFromNode.pop(node2)

		# print "Edge dict after contraction: " + str(self.edgesFromNode)
		# print "Edges after contraction: " + str(self.edges)
		# print "Nodes after contraction: " + str(self.nodes)

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
			originalGraph = Graph(inputFile, d)
	else:
		originalGraph = Graph(inputFile)
	inputFile.close()

	if args.n:
		numRuns = args.n
	else:
		numRuns = int(originalGraph.getNumNodes() * originalGraph.getNumNodes() * math.log(originalGraph.getNumNodes()))

	bestMinCut = sys.maxint
	for i in range(numRuns):
		print i
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

