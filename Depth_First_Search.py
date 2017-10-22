def Search(graph, root):
    """Runs depth-first search through a graph, starting at a given root.
    
    Args:
        graph: the given graph, with nodes encoded as strings.
        root: the node from which to start the search.
        
    Returns:
        A list of nodes in the order in which they were first visited.
    """
    stack = [root]  # We first put the root element in the stack
    parent = []  # Initializing the parent list as an empty list
    while stack:
        vertex = stack.pop() # Getting the last element of the stack(LIFO)
        if vertex not in parent:
            parent.append(vertex)  # Putting that element in the parent list
            for child in graph[vertex]: # Finding children of the node
                stack.append(child) # appending the children to the stack

    return parent  


def connected_components(graph):
    """Computes the connected components of the given graph.
    
    Args: 
        graph: the given graph, with nodes encoded as strings.
        
    Returns:
        The connected components of the graph. Components are listed in
        alphabetical order of their root nodes.
    """
    new = list(graph.nodes()) # List of all unvisited or 'new' nodes
    new.sort()  # Sorting to get the output desired
    connect_components = [] # Initializing
    while len(new) > 0: # This loop calls the 'Search' function on all nodes of the graph.
                                                 
            
            visit = Search(graph, new[0])   # Search the Graph starting at the first node
            
            connect_components.append(visit) # Add all the connected nodes in a list
        
            remain = list(set(new) - set(visit))  # Remove the visited 'new' nodes as 
                                                  # they are not new anymore.
                
            remain.sort()  # Sort the remaining nodes
            new = remain # Store these remaining values in new
                              
    return connect_components

