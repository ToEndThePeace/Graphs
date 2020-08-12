from graph import Graph
from util import Stack


def earliest_ancestor1(ancestors, starting_node):
    """
    Lookup Table - first pass implementation
    """
    ancestor_lookup = {}
    for a in ancestors:
        if a[0] not in ancestor_lookup:
            ancestor_lookup[a[0]] = []
        if a[1] not in ancestor_lookup:
            ancestor_lookup[a[1]] = [a[0]]
        else:
            ancestor_lookup[a[1]].append(a[0])
    # print(ancestor_lookup)
    print(ancestor_lookup)

    def get_ancestor(node):
        if len(ancestor_lookup[node]) == 0:
            if node == starting_node:
                return -1
            return node
        else:
            for i in ancestor_lookup[node]:
                # print(i, ancestor_lookup[i])
                return get_ancestor(i)

    return get_ancestor(starting_node)


def earliest_ancestor2(ancestors, starting_node):
    ancestor_graph = Graph()
    for i in ancestors:
        ancestor_graph.add_vertex(i[0])
        ancestor_graph.add_vertex(i[1])
    for i in ancestors:
        ancestor_graph.add_edge(i[1], i[0])
    # print(ancestor_graph)

    s = Stack()
    s.push([starting_node])
    possible_res = []

    while s.size() > 0:
        current = s.pop()
        for neighbor in ancestor_graph.get_neighbors(current[-1]):
            new_path = current + [neighbor]
            if len(ancestor_graph.vertices[neighbor]) == 0:
                possible_res.append(new_path)
            else:
                s.push(new_path)

    if len(possible_res) == 0:
        return -1

    res = possible_res[0]

    max_len = 0

    for x in possible_res:
        if len(x) >= max_len:
            res = x
            max_len = len(x)

    return res[-1]


earliest_ancestor = earliest_ancestor2
