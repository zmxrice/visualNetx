'''
Reference implementation of node2vec.

Author: Aditya Grover

For more details, refer to the paper:
node2vec: Scalable Feature Learning for Networks
Aditya Grover and Jure Leskovec
Knowledge Discovery and Data Mining (KDD), 2016
'''

import argparse
import numpy as np
import networkx as nx
import node2vec
from gensim.models import Word2Vec

def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run node2vec.")

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='emb/karate.emb',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')

	parser.add_argument('--walk-length', type=int, default=80,
	                    help='Length of walk per source. Default is 80.')

	parser.add_argument('--num-walks', type=int, default=10,
	                    help='Number of walks per source. Default is 10.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--iter', default=1, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--workers', type=int, default=8,
	                    help='Number of parallel workers. Default is 8.')

	parser.add_argument('--p', type=float, default=1,
	                    help='Return hyperparameter. Default is 1.')

	parser.add_argument('--q', type=float, default=1,
	                    help='Inout hyperparameter. Default is 1.')

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	return parser.parse_args()

def read_graph_weighted(path):
	'''
	Reads the input network in networkx.
	Modify the code to using clustering coefficient as the weight
	initially un-weighted graph, undirected graph
	'''
	G = nx.read_edgelist(path, nodetype=int)
	clusterCoefficient = nx.clustering(G)
	for edge in G.edges():
		G[edge[0]][edge[1]]['weight'] = clusterCoefficient[edge[0]] + clusterCoefficient[edge[1]]

	return G

def read_graph(path):
	if args.weighted:
		G = nx.read_edgelist(path, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
	else:

		G = nx.read_edgelist(path, nodetype=int, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not args.directed:
		G = G.to_undirected()

	return G

import csv
import random
def genNegGraph():
	G = read_graph(args.input)
	edges = G.edges()
	nodes = G.nodes()
	n = len(edges)
	neg_Graph = nx.Graph()
	cnt = 0
	while cnt < n:
		node1, node2 = random.choice(nodes), random.choice(nodes)
		if node1 != node2 and not G.has_edge(node1, node2):
			neg_Graph.add_edge(node1,node2)
			cnt += 1
	nx.write_edgelist(neg_Graph, "graph/negative.edgelist")
	return neg_Graph

def genEdgeFeatures(args):
	G = read_graph(args.input)
	neg_G = read_graph("graph/negative.edgelist")

	f = open(args.output, "rb")
	f.readline()
	node_features = {}
	for line in f:
		cur = map(float, line.split())
		node_features[cur[0]] = np.array(cur[1:])

	f.close()
	# jaccards
	csvfile = open('emb/karate_jc.csv', 'wb')
	wter = csv.writer(csvfile, delimiter=',')
	wter.writerow(["feature", "class"])

	preds = nx.jaccard_coefficient(G, G.edges())

	for x, y, p in preds:
		wter.writerow([p, "pos"])

	preds = nx.jaccard_coefficient(G, neg_G.edges())

	for x, y, p in preds:
		wter.writerow([p, "neg"])

	csvfile.close()

	# resource allocation
	csvfile = open('emb/karate_ra.csv', 'wb')
	wter = csv.writer(csvfile, delimiter=',')
	wter.writerow(["feature", "class"])

	preds = nx.resource_allocation_index(G, G.edges())

	for x, y, p in preds:
		wter.writerow([p, "pos"])

	preds = nx.resource_allocation_index(G, neg_G.edges())

	for x, y, p in preds:
		wter.writerow([p, "neg"])

	csvfile.close()

	# adamic adar
	csvfile = open('emb/karate_aa.csv', 'wb')
	wter = csv.writer(csvfile, delimiter=',')
	wter.writerow(["feature", "class"])

	preds = nx.adamic_adar_index(G, G.edges())

	for x, y, p in preds:
		wter.writerow([p, "pos"])

	preds = nx.adamic_adar_index(G, neg_G.edges())

	for x, y, p in preds:
		wter.writerow([p, "neg"])

	csvfile.close()

	# preferential attachment
	csvfile = open('emb/karate_pref.csv', 'wb')
	wter = csv.writer(csvfile, delimiter=',')
	wter.writerow(["feature", "class"])

	preds = nx.preferential_attachment(G, G.edges())

	for x, y, p in preds:
		wter.writerow([p, "pos"])

	preds = nx.preferential_attachment(G, neg_G.edges())

	for x, y, p in preds:
		wter.writerow([p, "neg"])

	csvfile.close()


	# random walk
	csvfile = open('emb/karate.csv', 'wb')
	#csvfile = open('emb/karate_cluster.csv', 'wb')
	wter = csv.writer(csvfile, delimiter=',')
	first = ["feature "+ str(i) for i in range(len(node_features.values()[0]))]
	wter.writerow(first+["class"])
	for x, y in G.edges():
		wter.writerow(list(node_features[x] * node_features[y]) + ["pos"])

	for x, y in neg_G.edges():
		wter.writerow(list(node_features[x] * node_features[y]) + ["neg"])

	csvfile.close()

def learn_embeddings(walks, outPath):
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	walks = [map(str, walk) for walk in walks]
	model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, sg=1, workers=args.workers, iter=args.iter)
	model.save_word2vec_format(outPath)

	return

def getNodeFeatures(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''
	nx_G = read_graph(args.input)
	#nx_G = read_graph_weighted(args.input)
	G = node2vec.Graph(nx_G, args.directed, args.p, args.q)
	G.preprocess_transition_probs()
	walks = G.simulate_walks(args.num_walks, args.walk_length)
	learn_embeddings(walks, "emb/karate_init.emb")
	#learn_embeddings(walks, "emb/karate_cluster.emb")



if __name__ == "__main__":
	args = parse_args()
	#genNegGraph()
	getNodeFeatures(args)
	genEdgeFeatures(args)
