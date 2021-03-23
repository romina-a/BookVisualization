from CharacterNames import create_character_MultiGraph, merge_similar_nodes
from DrawGraph import draw_graph_plotly as draw
from GraphProssesing import draw_graph_through_time

import time
import os
import networkx as nx
import GraphProssesing
import argparse

# TODO make more usable


# 1. determine the book address
# book_address = "./Data/HarryPotter/Cleaned/J K Rowling___1. Harry Potter and the Philosophers Stone.txt"
book_address = "./Data/Gutenberg/txt/Charles Dickens___Oliver Twist.txt"
# book_address = "./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt"
# book_address = "./Data/Gutenberg/txt/Sir Arthur Conan Doyle___The Hound of the Baskervilles.txt"


def extract_book_name_from_adr(adr):
    file_name = os.path.split(adr)[-1]
    name = os.path.splitext(file_name)[0]
    return name


def do_all(book_adr):
    # book name is automatically set
    book_name = extract_book_name_from_adr(book_adr)

    # create the graph and use useful functions

    # create and save the raw graph
    print("creating the graph...")
    t = time.time()
    G = create_character_MultiGraph(book_adr)
    print("%%%% took:{}s".format(time.time()-t))

    # save the graph, can load with G_Sim = nx.read_gpickle("<adr>/<name>.gpickle")
    nx.write_gpickle(G, f'./SavedGraphs/{book_name}.gpickle')

    # print the extracted names
    print("Raw graph nodes (before merging):")
    print("name\t count")
    for i in list(G):
        print(f'{i}\t{G.nodes[i]["count"]}')
    print()

    # draw the raw graph
    draw(G, book_name+': Raw Graph')

    # merge node
    merge_similar_nodes(G)

    # print nodes after merge
    print("graph nodes after merging")
    print("name\t count")
    for i in list(G):
        print(f'{i}\t{G.nodes[i]["count"]}')
    print()

    # print the merged ones
    print("merged nodes:")
    for i in list(G):
        if "contraction" in G.nodes[i]:
            print(f'{i}\t{list(G.nodes[i]["contraction"].keys())}')
    print()

    # draw the merged graph
    draw(G, book_name+': Merged Graph')

    # draw largest connected component
    largest_cc = max(nx.connected_components(G), key=len)
    G_main = G.subgraph(largest_cc).copy()
    draw(G_main, book_name+': Merged Graph largest connected component')

    # print highest degree nodes:
    highs = GraphProssesing.find_highest_deg(G, 20)
    print("highest degree nodes are:\n\t{}".format(highs))

    # draw highest degree character graph
    G_high = G.subgraph(dict(highs).keys())
    draw(G_high, 'after merging highest degree nodes')

    GraphProssesing.plot_degree_dist(G)

    GraphProssesing.plot_topk_pagerank_history(G, num_of_snapshots=30, k=3)

    # Story narration
    # draw_graph_through_time(G_Sim, 30, pagerank_threshold=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-address", required=False, default=book_address,
                    help="path to the book")
    args = vars(parser.parse_args())
    book_adr = args['book_address']
    do_all(book_adr)
