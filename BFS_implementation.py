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

