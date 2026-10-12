import heapq

inf = 10**9

city_names = ['u', 'v', 'w', 'x', 'y', 'z']

# structure representing a node in the state space tree
class Node:
    def __init__(self, n=0):

        # reduced cost matrix
        self.matrix = [[inf] * n for _ in range(n)]

        # lower bound cost of this node
        self.cost = 0

        # current city
        self.vertex = 0

        # number of cities visited so far
        self.level = 0

        # path taken to reach this node
        self.path = []

    def __lt__(self, other):
        return self.cost < other.cost

# reduce rows and columns of matrix, return total reduction cost
def reduce_matrix(mat):

    n = len(mat)
    reduction = 0

    # row reduction
    for i in range(n):

        row_min = min(mat[i])

        # subtract row minimum from all elements of that row
        if row_min != inf and row_min > 0:

            reduction += row_min

            for j in range(n):
                if mat[i][j] != inf:
                    mat[i][j] -= row_min

    # column reduction
    for j in range(n):

        col_min = min(mat[i][j] for i in range(n))

        # subtract column minimum from all elements of that column
        if col_min != inf and col_min > 0:

            reduction += col_min

            for i in range(n):
                if mat[i][j] != inf:
                    mat[i][j] -= col_min

    # return total reduction cost which contributes to lower bound
    return reduction


# create a child node after moving from one city to another
def create_child(parent, from_city, to):

    n = len(parent.matrix)
    child = Node(n)

    # copy parent reduced matrix
    child.matrix = [row[:] for row in parent.matrix]

    # disable all outgoing edges from current city
    for j in range(n):
        child.matrix[from_city][j] = inf

    # disable all incoming edges to the next city
    for i in range(n):
        child.matrix[i][to] = inf

    # cost of edge used for transition
    edge_cost = parent.matrix[from_city][to]

    # new cost includes parent cost and edge cost
    child.cost = parent.cost + edge_cost

    # perform reduction on the new matrix
    reduction = reduce_matrix(child.matrix)

    # add reduction cost to obtain lower bound
    child.cost += reduction

    # update node information
    child.vertex = to
    child.level = parent.level + 1

    # copy path and append new city
    child.path = parent.path[:]
    child.path.append(to)

    return child


# solve tsp using branch and bound
def solve_tsp(cost_matrix):

    n = len(cost_matrix)

    # create root node
    root = Node(n)
    root.matrix = [row[:] for row in cost_matrix]
    root.vertex = 0
    root.level = 0

    # starting city
    root.path.append(0)

    # compute initial reduction
    root.cost = reduce_matrix(root.matrix)

    # priority queue to select node with smallest bound
    pq = []
    heapq.heappush(pq, root)

    best_cost = inf
    best_path = []

    # explore nodes until queue becomes empty
    while pq:

        cur = heapq.heappop(pq)

        # prune nodes whose bound is already worse
        if cur.cost >= best_cost:
            continue

        # if all cities are visited
        if cur.level == n - 1:

            # cost to return to starting city
            final_edge = cur.matrix[cur.vertex][0]

            if final_edge == inf:
                continue

            total_cost = cur.cost + final_edge

            # update best solution
            if total_cost < best_cost:

                best_cost = total_cost
                best_path = cur.path[:]
                best_path.append(0)

            continue

        # expand current node to all possible next cities
        for j in range(n):

            if cur.matrix[cur.vertex][j] != inf:

                visited = j in cur.path

                if visited:
                    continue

                # create child node
                child = create_child(cur, cur.vertex, j)

                # push only promising nodes
                if child.cost < best_cost:
                    heapq.heappush(pq, child)

    return best_cost, best_path


if __name__=="__main__":
    cost_matrix = [
        [0, 51, 56, 60, 2, 35],
        [51, 0, 78, 13, 51, 68],
        [56, 78, 0, 70, 57, 21],
        [60, 13, 70, 0, 61, 68],
        [2, 51, 57, 61, 0, 36],
        [35, 68, 21, 68, 36, 0]
    ]
    
    best_cost, path = solve_tsp(cost_matrix)
    
    if best_cost >= inf:
        print("No Hamiltonian cycle found")
    else:
        print("Minimum cost:", best_cost)
        named_path = [city_names[i] for i in path]
        print("Path:", " -> ".join(named_path))