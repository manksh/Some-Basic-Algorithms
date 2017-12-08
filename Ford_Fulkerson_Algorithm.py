import networkx as nx
G = nx.Graph()

usa = open('contiguous-usa.dat')
for line in usa:
    s1, s2 = line.strip().split()
    G.add_edge(s1, s2)

for state in G.nodes():
    if state != 'CA':
        G.node[state]['demand'] = 1
G.node['CA']['demand'] = -48

G = nx.DiGraph(G)
uniform_capacity = 16
for m in G.edges():
    G.edges[m[0]][m[1]]['capacity'] = uniform_capacity

def initialization(G):
    """ This function initialize a flow equal to zero on each edge of a given graph G """
    keys = []
    values = []
    for s1 in G.nodes():
        keys.append(s1)
        res = dict()
        for (s0, s2) in G.edges():
            if s0 == s1:
                res[s2] = 0
        values.append(res)
    flow = dict()
    for i, k in enumerate(keys):
        flow[k] = values[i]
    return flow

def Get_residual_graph(G, flow):
    """ Compute the residual graph for a given graph G crossed by a flow """
    G_res = nx.DiGraph()
    for (s1, s2) in G.edges():
        if flow[s1][s2] > 0:
            #Create a reversed edge in G_res with the value of the flow
            G_res.add_edges(s2, s1)
            G_res[s2][s1]['capacity'] = flow[s1][s2]

        if flow[s1][s2] < G[s1][s2]['capacity']:
            #Create in G_res a forward edge with the residual capacity
            G_res.add_edge(s1, s2)
            G_res[s1][s2]['capacity'] = G[s1][s2]['capacity'] - flow[s1][s2]

    return G_res

def BFS(G, root):
    """ Compute a BFS in graph G from vertex root and returns the list of predecessors and the connected
    component of root"""
    queue = [root]
    discovered = [root]
    prev = dict()
    while len(queue) > 0:
        u = queue[0]
        #Get rid of the first element
        queue = queue[1:]
        for v in G.neighbors(u):
            if v not in discovered:
                prev[v] = u
                discovered.append(v)
                queue.append(v)
    return [prev, discovered]

def Find_Path(s, t, G):
    """ Given a graph and two vertices (s,t) this function will return an (s,t) path if it exists and None if not"""
    prev, discovered = BFS(G, s)
    if t not in discovered:
        return None
    else:
        path = [t]
        key = t
        while key != None:
            if key in prev.keys():
                path.append(prev[key])
                key = prev[key]
            else:
                key = None
        return path[::-1]

def Augment_flow(path, G_res, G, flow):
    """ Given a path in the residual graph and a flow in the real graph, this function returns
    the new augmented flow """
    capacities = []
    for k in range(len(path)-1):
        s1 = path[k]
        s2 = path[k+1]
        capacities.append(G_res.edge[s1][s2]['capacity'])
    add_flow = min(capacities)
    for k in range(len(path)-1):
        s1 = path[k]
        s2 = path[k+1]
        if (s1, s2) in G.edges():
            flow[s1][s2] = flow[s1][s2] + add_flow
        else:
            flow[s2][s1] = flow[s2][s1] - add_flow
    return flow


def flow_with_demands(graph):
    """Computes a flow with demands over the given graph.

    Args:
        graph: A directed graph with nodes annotated with 'demand' properties and edges annotated with 'capacity'
            properties.

    Returns:
        A dict of dicts containing the flow on each edge. For instance, flow[s1][s2] should provide the flow along
        edge (s1, s2).

    Raises:
        NetworkXUnfeasible: An error is thrown if there is no flow satisfying the demands.
    """
    # We begin by verifying the necessary condition: demand=offer
    test = []
    for state in graph.nodes():
        test.append(graph.node[state]['demand'])

    if sum(test) != 0:
        raise nx.NetworkXUnfeasible("No Feasible flow")

    # Creation of a super source
    G = graph.copy()
    G.add_node('S')
    for state in G.nodes():
        if state != 'S':
            if G.node[state]['demand'] < 0:
                G.add_edge('S', state)
                G.edge['S'][state]['capacity'] = -G.node[state]['demand']

    # Creation of a super sink
    G.add_node('T')
    for state in G.nodes():
        if state != 'S' and state != 'T':
            if G.node[state]['demand'] > 0:
                G.add_edge(state, 'T')
                G.edge[state]['T']['capacity'] = G.node[state]['demand']

    # Initialization of a flow equal to zero on every edge
    flow = initialization(G)

    # Compute first residual graph
    G_res = Get_residual_graph(G, flow)
    path = Find_Path('S', 'T', G_res)
    while path != None:
        # Find an augmenting flow
        flow = Augment_flow(path, G_res, G, flow)

        # Compute the corresponding residual graph
        G_res = Get_residual_graph(G, flow)

        # Compute the S-T path in the new residual graph
        path = Find_Path('S', 'T', G_res)


        # Verification that the max flow answers the demand
    demand = 0
    for state in G.nodes():
        if state != 'S' and state != 'T':
            if G.node[state]['demand'] > 0:
                demand += G.node[state]['demand']

    max_flow = 0
    for (s1, s2) in G.edges():
        if s1 == 'S':
            max_flow += flow['S'][s2]

    # Final Test
    if max_flow == demand:
        # Remove S and T from the flow
        for key in flow.keys():
            if 'T' in flow[key].keys():
                del flow[key]['T']
            if 'S' in flow[key].keys():
                del flow[key]['S']
        del flow['S']
        del flow['T']
        return flow
    else:
        raise nx.NetworkXUnfeasible("No Feasible Flow")