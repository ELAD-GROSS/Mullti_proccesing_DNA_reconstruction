from Improvement.Induced_Graph import InducedGraphAux
from Improvement.FinalDirectedGraph import FinalDirectedGraph
from Improvement.DynamicProgramming import create_guesses


def final_algorithm(strand_len, read_size, real_edge_length, reads_lst):
    # build induced graph
    data_for_induced_graph = InducedGraphAux(read_size, real_edge_length, reads_lst)
    induced_graph = data_for_induced_graph.build_induced_graph_from_data()

    # build final directed graph
    final_directed_graph = FinalDirectedGraph(induced_graph)

    keys_size = len(final_directed_graph.dict_graph.keys())

    for vertex in final_directed_graph.dict_graph.keys():
        if keys_size == 1:
            break
        if len(vertex) == strand_len:
            return {vertex}

    return create_guesses(final_directed_graph, strand_len)
