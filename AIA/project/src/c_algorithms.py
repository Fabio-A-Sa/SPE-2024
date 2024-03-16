from time import time
from collections import deque
from math import inf
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go

DIRECTIONS = {
    "up": (-1, 0),
    "left": (0, -1),
    "down": (1, 0),
    "right": (0, 1),
}

DIRECTION_OPOSITE = {
    (-1, 0) : (1, 0),
    (1, 0) : (-1, 0),
    (0, -1) : (0, 1),
    (0, 1) : (0, -1),
}

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def __hash__(self):
        return hash((tuple(tuple(inner_list) for inner_list in self.state)))

class BoardManipulator:
    """
    Contains the game logic and the shared functions between the algorithms
    """
    def __init__(self):
        self.tree_nodes = []

    def check_neighbor_piece(self, board, coordinates, cluster, direction):
        y, x = coordinates
        delta_y, delta_x = direction
        new_x = max(0, x + delta_x)
        new_y = max(0, y + delta_y)

        try:
            if board[new_y][new_x] == board[y][x] and cluster[new_y][new_x] == 0:
                cluster[new_y][new_x] = 1
                for new_direction in DIRECTIONS.values():
                    self.check_neighbor_piece(board, (new_y, new_x), cluster, new_direction)
        except:
            return None

    def get_cluster(self,board, coordinates):
        if board[coordinates[0]][coordinates[1]] == None:
            return []
        cluster = [[0 for _ in range(len(board))] for _ in range(len(board))]
        cluster[coordinates[0]][coordinates[1]] = 1
        for direction in DIRECTIONS.values():
            self.check_neighbor_piece(board, coordinates, cluster, direction)

        return cluster
    
    def move(self, board, coordinates, direction):
        
        side_size = len(board)

        cluster = self.get_cluster(board, coordinates)
        if cluster == []:
            return None

        new_board = [[None for _ in range(side_size)] for _ in range(side_size)]
        for i in range(0, side_size):
            for j in range(0, side_size):
                if cluster[i][j] == 1:
                    new_board[i][j] = None
                else:
                    new_board[i][j] = board[i][j]

        if direction == "up":
            for i in range(0, side_size):
                if cluster[0][i] == 1:
                    return None
                
            cluster.pop(0)
            line = [0 for _ in range(side_size)]
            cluster.append(line)

        elif direction == "down":
            for i in range(0, side_size):
                if cluster[side_size - 1][i] == 1:
                    return None
            for i in range(side_size - 1, -1, -1):
                for j in range(0, side_size):
                    cluster[i][j] = cluster[i - 1][j]
            for i in range(0, side_size):
                cluster[0][i] = 0

        elif direction == "left":
            for i in range(0, side_size):
                if cluster[i][0] == 1:
                    return None
            for i in range(0, side_size):
                for j in range(0, side_size - 1):
                    cluster[i][j] = cluster[i][j + 1]
            for i in range(0, side_size):
                cluster[i][side_size - 1] = 0

        elif direction == "right":
            for i in range(0, side_size):
                if cluster[i][side_size - 1] == 1:
                    return None
            for i in range(0, side_size):
                for j in range(side_size - 1, -1, -1):
                    cluster[i][j] = cluster[i][j - 1]
            for i in range(0, side_size):
                cluster[i][0] = 0

        color = board[coordinates[0]][coordinates[1]]

        for i in range(0, side_size):
            for j in range(0, side_size):
                if cluster[i][j] == 1:
                    if new_board[i][j] == None:
                        new_board[i][j] = color
                    else:
                        return None

        return new_board
    
    def get_number_clusters(self, board):
        aux_board = []
        viewed_clusters = 0

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != None:
                    aux_board.append((i,j))
        
        while aux_board:
            i,j = aux_board[0]  # get first element
            cluster = self.get_cluster(board, (i,j))
            if cluster == []: continue
            viewed_clusters += 1
            for a, row in enumerate(cluster):
                for b, _ in enumerate(row):
                    if cluster[a][b] == 1:
                        aux_board.remove((a,b))
        
        return viewed_clusters

    def get_number_colors(self, board):
        elements = set()
        for line in board:
            for element in line:
                elements.add(element)

        return elements.__len__() - 1

    def child_states(self, board):
        new_states = []
        aux_board = []

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != None:
                    aux_board.append((i,j))
        
        while aux_board:
            i,j = aux_board[0]  # get first element
            cluster = self.get_cluster(board, (i,j))
            for a, row in enumerate(cluster):
                for b, _ in enumerate(row):
                    if cluster[a][b] == 1:
                        aux_board.remove((a,b))
            
            for direction in DIRECTIONS.keys():
                    next_board = self.move(board, (i, j), direction)
                    if next_board:
                        new_states.append(next_board)
        
        return new_states

    def win(self, board):
        return self.get_number_clusters(board) == self.get_number_colors(board)

    def get_steps(self, solution : TreeNode):
        steps_counter = -1
        steps = []
        while solution:
            steps.append(solution.state)
            steps_counter += 1
            solution = solution.parent
        steps.reverse()

        return steps_counter, steps

    def depth(self, node) -> int:
        depth = 0
        while node.parent is not None:
            node = node.parent
            depth += 1
        return depth
    
    def timed_out(self, before) -> bool:
        return time() - before > 60

    def show_graph(self):

        labels = []

        G = Graph()

        def add_node(node, depth):
            state = node.state
            flat_state = ['w' if item is None else str(item) for sublist in state for item in sublist + [' ']]
            state_str = str(depth) + ': ' + ''.join(flat_state)

            G.add_vertex(state_str)
            labels.append(state_str)
            for child in node.children:
                add_node(child, depth+1)
                child_state = child.state
                c_flat_state = ['w' if item is None else str(item) for sublist in child_state for item in sublist + [' ']]
                c_state_str = str(depth+1) + ': ' + ''.join(c_flat_state)
                G.add_edge(state_str, c_state_str)

        solution_nodes = []
        nodes = self.tree_nodes

        depth = self.depth(nodes)

        while True:
            state = nodes.state
            flat_state = ['w' if item is None else str(item) for sublist in state for item in sublist + [' ']]
            state_str = str(depth) + ': ' + ''.join(flat_state)

            solution_nodes.append(state_str)
            if(nodes.parent) is None: break
            nodes = nodes.parent
            depth -= 1

        add_node(nodes, 0)
        lay = G.layout('rt')

        nr_vertices = G.vcount()

        position = {k: lay[k] for k in range(nr_vertices)}
        Y = [lay[k][1] for k in range(nr_vertices)]
        M = max(Y)
        es = EdgeSeq(G)  # sequence of edges
        E = [e.tuple for e in es]  # list of edges
        L = len(position)

        Xn = [position[k][0] for k in range(L)]
        Yn = [M - position[k][1] for k in range(L)]
        Xe = []
        Ye = []

        for edge in E:
            Xe += [position[edge[0]][0], position[edge[1]][0], None]
            Ye += [M - position[edge[0]][1], M - position[edge[1]][1], None]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Xe, y=Ye, mode='lines', line=dict(color='rgb(210,210,210)', width=1), hoverinfo='none'))

        colors = []

        for label in labels:
            if label in solution_nodes:
                colors.append('#FF0000')
            else:
                colors.append('#6175c1')

        fig.add_trace(go.Scatter(x=Xn, y=Yn, mode='markers', name='Node', marker=dict(symbol='circle-dot', size=18, color=colors,line=dict(color='rgb(50,50,50)', width=1)),
                                text=labels, hoverinfo='text', opacity=0.8))

        fig.show()

    def search_heuristic_1(self, board):
        return self.get_number_clusters(board) - self.get_number_colors(board)
    
    def search_heuristic_2(self, board):
        clusters = []
        for (i, j) in [(i, j) for i in range(len(board)) for j in range(len(board))]:
            cluster = self.get_cluster(board, [i, j])
            if cluster == []:
                continue
            if (cluster, board[i][j]) not in clusters:
                clusters.append((cluster, board[i][j]))

        total = 0
        for i1 in range(0, len(clusters)-1):
            for i2 in range(i1+1, len(clusters)):
                (cluster1, color1), (cluster2, color2) = clusters[i1], clusters[i2]
                if color1 == color2:
                    total += self.get_distance(cluster1, cluster2)

        return total

    def search_heuristic_3(self, board):
        return self.a_star_search_heuristic1(board) * len(board)


class ASTAR(BoardManipulator):
    def __init__(self):
        super().__init__()
    
    def run(self, board : list, score : list) -> None: # The result is stored in the score list
        self.before = time()
        score[0] = "*"
        score[1] = "*"
        nodes = self.a_star_search(board, self.win, self.child_states, self.search_heuristic_2)
        if nodes is None:
            score[0] = "N/A"
            score[1] = "N/A"
        else:
            self.tree_nodes = nodes
            score[0] = round(time() - self.before, 2) # Time
            score[1], score[3] = self.get_steps(nodes) # Moves and Board states for each move
            score[5] = True # Solved
            
    def shortest_path(self, initial_coordinate, cluster):
        visited = set()
        queue = deque([(initial_coordinate, [])])

        while queue:
            (row, col), path = queue.popleft()
            if (row, col) in visited:
                continue
            visited.add((row, col))

            if cluster[row][col] == 1:
                return len(path)

            for vx, vy in DIRECTIONS.values():
                next_x, next_y = row + vx, col + vy
                if 0 <= next_x < len(cluster) and 0 <= next_y < len(cluster) and (next_x, next_y) not in visited:
                    queue.append(((next_x, next_y), path + [(row, col)]))

        return None

    def get_distance(self, cluster1, cluster2):
        total = inf
        for (i, j) in [(i, j) for i in range(len(cluster1)) for j in range(len(cluster1))]:
            if cluster1[i][j] == 1:
                total = min(self.shortest_path((i, j), cluster2), total)
        return total

    def a_star_search(self, initial_state, goal_state_func, operators_func, heuristic_func):

        root = TreeNode(initial_state)  # create the root node in the search tree
        stack = [(root, heuristic_func(initial_state))]  # initialize the queue to store the nodes
        filtered_states = [initial_state]

        while len(stack):

            if self.timed_out(self.before): return None

            node, _ = stack.pop()  # get first element in the queue
            #print("nó com valor", v)
            if goal_state_func(node.state):  # check goal state
                return node

            children = operators_func(node.state)
            evaluated_children = [(child, heuristic_func(child) + self.depth(node) + 1) for child in children]

            for (child, value) in evaluated_children:  # go through next states
                if child in filtered_states:
                    continue
                
                filtered_states.append(child)

                # create tree node with the new state
                child_tree = TreeNode(child, node)

                node.add_child(child_tree)

                # enqueue the child node
                stack.append((child_tree, value))
            
            stack = sorted(stack, key = lambda node: node[1], reverse=True)

        return None

class BFS(BoardManipulator):
    def __init__(self):
        super().__init__()
    
    def run(self, board : list, score : list):
        self.before = time()
        score[0] = "*"
        score[1] = "*"
        nodes = self.breadth_first_search(initial_state=board,
                                                  goal_state_func=self.win,
                                                  operators_func=self.child_states)
        if nodes is None:
            score[0] = "N/A"
            score[1] = "N/A"
        else:
            self.tree_nodes = nodes
            score[0] = round(time() - self.before, 2) # Time
            score[1], score[3] = self.get_steps(nodes) # Moves and Board states for each move
            score[5] = True # Solved

    def breadth_first_search(self, initial_state, goal_state_func, operators_func):
        root = TreeNode(initial_state)  # create the root node in the search tree
        queue = deque([root])  # initialize the queue to store the nodes
        visited = [initial_state]

        while queue:  # while the queue is not empty

            if self.timed_out(self.before): return None

            node = queue.popleft()  # get first element in the queue
            if goal_state_func(node.state):  # check goal state
                return node

            for state in operators_func(node.state):
                if state not in visited:  # go through next states
                    child = TreeNode(state=state, parent=node)
                    node.add_child(child)
                    queue.append(child)
                    visited.append(state)

        return None  # no solution found
    
class DFS(BoardManipulator):
    def __init__(self):
        super().__init__()
    
    def run(self, board : list, score : list):
        self.before = time()
        score[0] = "*"
        score[1] = "*"
        nodes = self.depth_first_search(board, self.win, self.child_states)
        if nodes is None:
            score[0] = "N/A"
            score[1] = "N/A"
        else:
            self.tree_nodes = nodes
            score[0] = round(time() - self.before, 2) # Time
            score[1], score[3] = self.get_steps(nodes) # Moves and Board states for each move
            score[5] = True # Solved

    def depth_first_search(self, initial_state, goal_state_func, operators_func):
        root = TreeNode(initial_state) # create the root node in the search tree
        stack = [root] # initialize the stack to store the nodes
        filtered_states = [initial_state]

        while stack:  # while the stack is not empty

            if self.timed_out(self.before): return None

            node = stack.pop() # get last element in the stack
            if goal_state_func(node.state): # check goal state
                return node

            for state in operators_func(node.state): # go through next states
                if state in filtered_states:
                    continue
                else:
                    filtered_states.append(state)

                # create tree node with the new state
                child_tree = TreeNode(state, node)

                # link child node to its parent in the tree
                node.add_child(child_tree)

                # push the child node to the stack
                stack.append(child_tree)

        return None # no solution found

class GREEDY(BoardManipulator):
    def __init__(self):
        super().__init__()
    
    def run(self, board : list, score : list) -> None: # The result is stored in the score list
        self.before = time()
        score[0] = "*"
        score[1] = "*"
        nodes = self.greedy_search(board, self.win, self.child_states, self.search_heuristic_1)

        if nodes is None:
            score[0] = "N/A"
            score[1] = "N/A"
        else:
            self.tree_nodes = nodes
            score[0] = round(time() - self.before, 2) # Time
            score[1], score[3] = self.get_steps(nodes) # Moves and Board states for each move
            score[5] = True # Solved
    
    def greedy_search(self, initial_state, goal_state_func, operators_func, heuristic_func):

        root = TreeNode(initial_state)  # create the root node in the search tree
        stack = [(root, heuristic_func(initial_state))]  # initialize the queue to store the nodes
        filtered_states = [initial_state]

        while len(stack):

            if self.timed_out(self.before): return None

            node, v = stack.pop()  # get first element in the queue
            if goal_state_func(node.state):  # check goal state
                return node

            children = operators_func(node.state)
            evaluated_children = [(child, heuristic_func(child)) for child in children]

            for (child, value) in evaluated_children:  # go through next states
                if child in filtered_states:
                    continue
                
                filtered_states.append(child)

                # create tree node with the new state
                child_tree = TreeNode(child, node)

                node.add_child(child_tree)

                # enqueue the child node
                stack.append((child_tree, value))

            stack = sorted(stack, key = lambda node: node[1], reverse=True)

        return None
