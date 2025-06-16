import os
import networkx as nx
from spmf import Spmf
from networkx.algorithms import isomorphism

from transcription import *

def is_subgraph_of(
    small: nx.Graph,
    big: nx.Graph,
    node_attr: str = "label",
    edge_attr: str = "label",
) -> bool:
    gm = isomorphism.GraphMatcher(
        big,
        small,
        node_match=isomorphism.categorical_node_match(node_attr, None),
        edge_match=isomorphism.categorical_edge_match(edge_attr, None),
    )
    if hasattr(gm, "subgraph_is_monomorphic"):
        return gm.subgraph_is_monomorphic()
    else:
        return any(True for _ in gm.subgraph_monomorphisms_iter())

def closed_frequent_graphs_canonical(
    patterns: list[tuple[nx.Graph, int]],
    node_attr: str = "label",
    edge_attr: str = "label",
) -> list[tuple[nx.Graph, int]]:
    support_groups = {}
    for idx, (_, sup) in enumerate(patterns):
        support_groups.setdefault(sup, []).append(idx)

    return [
        (g_i, sup_i)
        for i, (g_i, sup_i) in enumerate(patterns)
        if not any(
            i != j and is_subgraph_of(g_i, patterns[j][0], node_attr, edge_attr)
            for j in support_groups[sup_i]
        )
    ]

def cgSpan(graphs: list[nx.Graph], min_support: float, max_edges: int = 99, max_memory: int = 2048, node_attr: str = "label", edge_attr: str = "label", delete_spmf_files: bool = True, verbose: bool = False) -> list[tuple[nx.Graph, int]]:
    if verbose:
        print(f"Running cgSpan with min_support={min_support}, max_edges={max_edges}, max_memory={max_memory}MB, node_attr='{node_attr}', edge_attr='{edge_attr}'")
    
    ### Input validation
    if not graphs:
        print("No graphs provided to cgSpan.")
        return []
    if not isinstance(graphs, list):
        raise TypeError("The 'graphs' parameter must be a list of networkx.Graph objects.")
    for g in graphs:
        if not isinstance(g, nx.Graph):
            raise TypeError("All elements in 'graphs' must be networkx.Graph objects.")
        if g.number_of_edges() > max_edges:
            raise ValueError(f"Graph {g} has more edges than the maximum allowed ({max_edges}).")
    if min_support <= 0:
        raise ValueError("min_support must be greater than 0.")
    if max_edges <= 0:
        raise ValueError("max_edges must be greater than 0.")
    if max_memory <= 0:
        raise ValueError("max_memory must be greater than 0.")
    if not isinstance(min_support, (int, float)):
        raise TypeError("min_support must be an integer or a float.")
    if not isinstance(max_edges, int):
        raise TypeError("max_edges must be an integer.")
    if not isinstance(max_memory, int):
        raise TypeError("max_memory must be an integer.")
    if not isinstance(node_attr, str):
        raise TypeError("node_attr must be a string.")
    if not isinstance(edge_attr, str):
        raise TypeError("edge_attr must be a string.")
    if not isinstance(delete_spmf_files, bool):
        raise TypeError("delete_spmf_files must be a boolean.")
    if not isinstance(verbose, bool):
        raise TypeError("verbose must be a boolean.")
    if min_support > 1:
        raise ValueError("min_support must be between 0 and 1 (inclusive).")

    ### Prepare SPMF input and output file names
    FILE_GSPAN_NAME_IN = "gSpan_input.txt"
    FILE_GSPAN_NAME_OUT = "gSpan_output.txt"
    if verbose:
        print(f"Input file: {FILE_GSPAN_NAME_IN} created")
        print(f"Output file: {FILE_GSPAN_NAME_OUT} created")

    ### Graphs to SPMF format
    write_graphs_to_spmf(graphs, FILE_GSPAN_NAME_IN, with_freq=False)
    if verbose:
        print(f"Graphs written to {FILE_GSPAN_NAME_IN}")

    ### gSpan
    os.system(f"touch {FILE_GSPAN_NAME_IN}")
    spmf_GSpan = Spmf(
        algorithm_name="GSPAN",
        input_filename=FILE_GSPAN_NAME_IN,
        output_filename=FILE_GSPAN_NAME_OUT,
        arguments=[
            str(min_support), str(max_edges),
            "false", "false", "true"
        ],
        memory=max_memory
    )
    spmf_GSpan.run()
    if verbose:
        print(f"gSpan executed with min_support={min_support}, max_edges={max_edges}, max_memory={max_memory}MB")
    
    ### cgSpan
    cgSpan = closed_frequent_graphs_canonical(
        spmf_to_networkX_with_freq(FILE_GSPAN_NAME_OUT),
        node_attr=node_attr,
        edge_attr=edge_attr
    )
    if verbose:
        print(f"Closed frequent graphs extracted: {len(cgSpan)} patterns found")

    if delete_spmf_files:
        os.remove(FILE_GSPAN_NAME_IN)
        os.remove(FILE_GSPAN_NAME_OUT)
        if verbose:
            print(f"Temporary files removed")

    return cgSpan
    