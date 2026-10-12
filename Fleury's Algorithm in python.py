# Python program to print Eulerian Path or 
# Circuit using Fleury's Algorithm (Weighted Graph Adaptation)

# Function to remove edge u-v from the graph
def removeEdge(adj, u, v):
    for i in range(len(adj[u])):
        if adj[u][i][0] == v:
            adj[u].pop(i)
            break
    for i in range(len(adj[v])):
        if adj[v][i][0] == u:
            adj[v].pop(i)
            break

# DFS to count reachable vertices from v
def dfsCount(v, adj, visited):
    visited[v] = True
    for neighbor, weight in adj[v]:
        if not visited[neighbor]:
            dfsCount(neighbor, adj, visited)

# Check if edge u-v is a valid next edge to traverse
def isValidNextEdge(u, v, adj, totalV):
    if len(adj[u]) == 1:
        return True

    visited = [False] * totalV
    dfsCount(u, adj, visited)
    count1 = sum(visited)

    removeEdge(adj, u, v)

    visited = [False] * totalV
    dfsCount(u, adj, visited)
    count2 = sum(visited)

    # Add edge back
    adj[u].append((v, 0)) # Weight doesn't matter for validity check
    adj[v].append((u, 0))

    return count1 == count2

# Recursively collect the Eulerian path/circuit starting from u
def getEulerUtil(u, adj, edges, v):
    for i in range(len(adj[u])):
        next_node = adj[u][i][0]
        if isValidNextEdge(u, next_node, adj, v):
            edges.append([u, next_node])
            removeEdge(adj, u, next_node)
            getEulerUtil(next_node, adj, edges, v)
            break

# Function to return Eulerian trail or circuit
def getEulerTour(v, adj):
    start = 0
    # Find a vertex with odd degree if exists
    for i in range(v):
        if len(adj[i]) % 2 != 0:
            start = i
            break

    edges = []
    getEulerUtil(start, adj, edges, v)
    return edges

if __name__ == "__main__":
    num_vertices = 6
    
    adj = [[] for _ in range(num_vertices)]
    
    def add_edge(u, v, weight):
        adj[u].append((v, weight))
        adj[v].append((u, weight))
    
    add_edge(0, 3, 1)  # u - x (1)
    add_edge(0, 4, 4)  # u - y (4)
    add_edge(0, 2, 5)  # u - w (5)
    add_edge(3, 4, 2)  # x - y (2)
    add_edge(3, 5, 3)  # x - z (3)
    add_edge(3, 1, 6)  # x - v (6)
    add_edge(4, 5, 2)  # y - z (2)
    add_edge(4, 2, 1)  # y - w (1)
    add_edge(5, 2, 2)  # z - w (2)
    add_edge(5, 1, 3)  # z - v (3)
    add_edge(2, 1, 2)  # w - v (2)

    for i in range(num_vertices):
        adj[i].sort(key=lambda x: x[1])

    initial_adj = [list(neighbors) for neighbors in adj]

    res = getEulerTour(num_vertices, adj)

    node_names = {0: 'u', 1: 'v', 2: 'w', 3: 'x', 4: 'y', 5: 'z'}

    total_weight = 0
    path_str = ""

    print("Rute Euler yang ditemukan:")
    for i in range(len(res)):
        u, v = res[i]
        path_str += f"{node_names[u]}-{node_names[v]}"
        
        weight = 0
        for neighbor, w in initial_adj[u]:
            if neighbor == v:
                weight = w
                break
        total_weight += weight
        
        if i != len(res) - 1:
            path_str += ", "

    print(path_str)
    print(f"\nTotal Bobot (Minimum-Weight Tour): {total_weight}")