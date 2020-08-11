
def earliest_ancestor(ancestors, starting_node):
    ancestor_lookup = {}
    for a in ancestors:
        if a[0] not in ancestor_lookup:
            ancestor_lookup[a[0]] = []
        if a[1] not in ancestor_lookup:
            ancestor_lookup[a[1]] = [a[0]]
        else:
            ancestor_lookup[a[1]].append(a[0])
    # print(ancestor_lookup)

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