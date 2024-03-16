# **Cohesion Free** : Heuristic Search Methods for One Player Solitaire Games
# Grade: 20/20

The player has many different modes and difficults to choose:

![Cohesion](/images/cohesion.png)

The player has multiple algorithms to run:

![Game Start](/images/game.png)

An example of computed Search Tree of DFS algorithm:

![IA Search Algorithm 1](/images/dfs.png)

An example of computed Search Tree of A* algorithm:

![IA Search Algorithm 2](/images/search.png)

## Table of Contents

- [Game Definition](#game-definition)
- [Setup](#setup)
- [Usage](#usage)
- [Files](#files)
    - [\_\_main\_\_.py](#__main__py)
    - [levels.py](#levelspy)
    - [c_auxiliar_functions.py](#c_auxiliar_functionspy)
    - [c_display.py](#c_displaypy)
    - [c_draw.py](#c_drawpy)
    - [cohesion_free_logic.py](#cohesion_free_logicpy)
    - [c_algorithms.py](#c_algorithmspy)
        - [TreeNodes](#treenodes)
        - [MutualFunction](#mutualfunction)
        - [BFS](#bfs)
        - [DFS](#dfs)
        - [GREEDY](#greedy)
        - [ASTAR](#astar)


---

## Game Definition 

The game [Cohesion Free](https://play.google.com/store/apps/details?id=com.NeatWits.CohesionFree&hl=en&gl=US) is a one-player game played on a pre-generated board with four different colors. The game starts with a scrambled board, and the player must slide tiles to form larger clusters of tiles of the same color. The game ends when the player wins by having only a single cluster of each color.

## Setup

We used Python 3.10.10 to run the application, but it is expected to run with any version from Python 3.8-3.10 as well.
It was used [Pygame](https://www.pygame.org/news) to display the application and [plotly](https://plotly.com/python/) and [igraph](https://python.igraph.org/en/stable/) to generate the graphs of the algorithms.
You can install the necessary packages to run this application with the following command:
```bash
pip install -r requirements.txt
```

Alternatively, you can install each package manually with the following command:
```bash
pip install igraph pygame plotly
```

## Usage

In order to run the application, please run the `__main__.py` file inside the `src` folder on your IDE, or with the following command:
```bash
python3 src/__main__.py
# or
python src/__main__.py
```

## Files
The application is separated in different files for easier readability. Notice that in some files it was added a `c_*` before the name itself, this prevents any conflict between any other package of the same name you might have installed.

### \_\_main\_\_.py
This file is the entry point for the game. It runs first the Main menu, and only after selecting the level, does the game runs. If the level given by the menu is empty, then the infinite loop of the game is broken:

```python
while True: 
    ...

    # Run the game main menu and get the level chosen by the player
    level = menu.run()

    if level == []: break

    ...
```

Also, if the `game.run()` returns false, given by an intentional quit, the cycle is broken.

```python
while True: 
    ...

    game = draw.Game(level)

    # Run the game, if the game is over, break the loop
    if game.run(): break

```

### levels.py
This file contains the levels to be displayed on the game accordingly. Notice that the main menu limits the visualization of 15 levels, and every 5 levels represent a difficulty, ranging from easy to hard. This is an example of a level:
```python
LEVELS = {
    # Notice that the key represents the number of the level displayed in the game
    # And that 'None' represents a white space on the board
    1: [
        ['r', None, None, 'r'],
        ['b', 'r', 'r', 'b'],
        [None, 'b', 'b', None],
        ['y', None, None, 'y'],
    ],
    ...
}
```

### c_auxiliar_functions.py
This file contains auxiliar objects and functions that are used on the `c_display.py` and `c_draw.py` files:
```python
class Coordinate(object):
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    ...
    # Verifies is the Coordinate object is inside the Recantangle Coordinates
    def is_inside_rect(self, coordinates : RectValue) -> bool:
        x1, y1, width, height = coordinates.getAllCoordinates()
        x1 -= width//2
        y1 -= height//2
        return self.x >= x1 and self.x <= x1 + width and self.y >= y1 and self.y <= y1 + height
    ...

class ColorValue(object):
    def __init__(self, r, g, b) -> None:

        # Check if the color values are valid
        if r < 0 or g < 0 or b < 0:
            raise ValueError("The color values must be positive")
        
        if r > 255 or g > 255 or b > 255:
            raise ValueError("The color values must be equal or less than 255")

        # Set the color values
        self.r = r
        self.g = g
        self.b = b

        # Create a tuple with the color values
        self.color = [r, g, b]

    ...

class RectValue(object):
    def __init__(self,x1,y1,width,height) -> None:
        try:
            self.coordinates = Coordinate(x1,y1)
            self.dimensions = Coordinate(width,height)
        except ValueError as e:
            raise ValueError("Invalid coordinates for Rectangle") from e
    
    ...

    def getAllCoordinates(self) -> list:
        return self.coordinates.getX(), self.coordinates.getY(), self.dimensions.getX(), self.dimensions.getY()
```

### c_display.py
The class `Display` acts as an interface between the game and the pygame package itself. The constructor sets the screen dimensions, the clock, the fps, as well as 3 different fonts:

```python
def __init__(self, width : int = 1280, height : int = 720):

    # Initialize pygame
    pygame.init()

    # Set the display
    self.width = width
    self.height = height
    self.screen = pygame.display.set_mode((self.width, self.height))

    # Set the clock
    self.clock = pygame.time.Clock()

    # Set the fonts
    self.normal_font = pygame.font.SysFont("Arial", 50)
    self.bigger_font = pygame.font.SysFont("Arial", 100)
    self.smaller_font = pygame.font.SysFont("Arial", 25)

    # Set the fps
    self.fps = 60
```

The remaining functions of this class should be self-explanatory looking at the code and provided documentation

### c_draw.py
The class `MutualDrawFunctions` contains common functions to be used both in the main menu and the game itself. Sets the position of the elements on the screen, as well as obtains the events from the `Display` class. Draws the background with a changing gradient, and a grey rectangle where the content is displayed:
```python
class MutualDrawFunctions:
    ...
    def draw_background(self) -> None:
        ...

        # Fill the Screen with a gradient
        for y in range(self.display.get_height()):

             # Calculate the color at this row
            hue = (self.HUE_OFFSET + (y /self.display.get_height()/5) * 240) % 360
            color = self.display.get_color_object()
            color.hsla = (hue, 100, 50, 100)

            # Draw a horizontal line with this color
            self.display.draw_standart_line(color, (0, y), (self.display.get_width(), y))

        # Increment the hue offset
        self.HUE_OFFSET = (self.HUE_OFFSET + self.HUE_CHANGE_SPEED) % 360

        # Draw a rectangle for the content
        self.display.draw_rect(LIGHT_GREY, self.content_rectangle)

        ...
```

The class `MainMenu` contains the main menu entry point, as well as the instructions and level selection. After each tick, it retrieves the events that took place in the `pygame` and takes an action accordingly:
- If the Play button was selected, changes the screen to the level selection;
- If the Instructions button was selected, changes the screen to the instructions;
- If the back button was selected, changes the screen to the main menu;
- If a level was selected, breaks the cycle and returns the selected level;
- If a quit event was obtained, breaks the cycle and returns an empty list, representing no level was selected.

The class `Game` contains the Cohesion Free game logic. After each tick, it retrieves the events that took place in the `pygame` and takes an action accordingly:
- If a tile was selected, firstly verifies if it selected a colored one. Then checks where the mouse slid to and gets a position, from 'up', 'down', 'left' and 'right' and calls the game logic to verify the given move by the player. If the move is possible, updates the number of moves and the board to the new game state;
- If the back button was selected, quits the game and returns false, stating that the given quit action was meant to go back into the main menu;
- If a quit event was obtained, quits the game and returns true, stating that the intention was to close the game;
- If a algorithm was selected, freezes the button and starts a new thread, with the selected algorithm, that tries to solve the puzzle from the current state. If the algorithm returns a solution, the less/greater and show graph buttons will appear;
- If the less/greater button was selected on a given algorithm, updates the board state to the one given by the algorithm as well as the current movement, and resets the current movement of the other algorithms;
- If the reset button was selected, it restarts the timer, the moves, as well as the algorithms current move;
- If the show graph button was selected, it starts a new thread that will display the graph of the solved algorithm.

### cohesion_free_logic.py

The `Cohesion` class contains the logic of the puzzle game itself. It starts by storing the total number of each colored tiles:
```python
class Cohesion:
    def __init__(self, board) -> None:
        self.colors = {
                'r': 0,
                'b': 0,
                'g': 0,
                'y': 0
            }
        
        self.board = board
        for row in self.board:
            for element in range(len(row)):
                if row[element] != None:
                    self.colors[row[element]] += 1
        ...
```
For every move made by the player, it firstly gets the cluster selected by the player and its color, returning 0 if it was an empty space, which doesn't update the current number of moves and the new board:
```python
cluster = self.__get_cluster(coords)
if cluster == []:
    return 0

color = self.board[coords[0]][coords[1]]
```
Then, it creates an auxiliar board, copying the original board and removing the pieces of the cluster, changing to an empty space:
```python
new_board = deepcopy(self.board)

# Remove the cluster from the board
for i in range(0, self.side_dimension):
    for j in range(0, self.side_dimension):
        if cluster[i][j] == 1:
            new_board[i][j] = None
```
Afterwards, for the given direction, verifies if there is an empty space (returning 0 otherwise) on the adjacent tiles and updates the cluster position to those tiles. In the end, if all passed sucessfuly, the board is updated and returns 1, representing a new move:
```python
if direction == "up":
    for i in range(0, self.side_dimension - 1):
        if cluster[0][i] == 1:
            return 0

    for i in range(0, self.side_dimension - 1):
        for j in range(0, self.side_dimension):
            cluster[i][j] = cluster[i + 1][j]
    for i in range(0, self.side_dimension):
        cluster[self.side_dimension - 1][i] = 0
...
for i in range(0, self.side_dimension):
    for j in range(0, self.side_dimension):
        if cluster[i][j] == 1:
            if new_board[i][j] == None:
                new_board[i][j] = color
            else:
                return 0
            
self.board = new_board

return 1
```

The win condition is obtained when the number of clusters equals the number of colors.

### c_algorithms.py
This file contains a class to represent the `TreeNodes`, as well as a `MutualFunction` class. It also contains a class for every algorithm used. To note that every algorithm is ran with the `run()` function, and it retrieves from the algorithm the tree nodes obtained to solve the algorithm, or None, case it timed out, or simply doesn't meet the win condition. Also, since the algorithms are ran on new threads, it requires the `score` parameter to be a list, in order to manipulate the values directly in memory. This is an example of how to manipulate the score:
```python
def run(self, board : list, score : list):
    self.before = time()
    nodes = self.depth_first_search(board, self.win, self.child_states)
    if nodes is None: # If didn't find a solution
        score[0] = "N/A" # The time is N/A 
        score[1] = "N/A" # The number of moves is N/A
    else: # If a solution was found
        self.tree_nodes = nodes
        score[0] += round(time() - self.before, 2) # Time
        score[1], score[3] = self.get_steps(nodes) # Moves and Board states for each move
        score[5] = True # Solved
```

#### TreeNodes
The `TreeNodes` class contains a representation of the nodes. Each node can have `n` amount of children and only one parent:
```python
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

```

#### MutualFunction
The `MutualFunction` class contains shared functions used by the algorithms. It also has an updated and optimized version of the cohesion free logic. 

The `child_states` function retrieves every possible move direction from a given board:
```python
def child_states(self, board):
    possible_moves = []
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
                    possible_moves.append(next_board)
    
    return possible_moves
```

The `get_steps` function retrieves a list of board states from the initial to the end state, as well as the number of moves made:
```python
def get_steps(self, solution : TreeNode):
    moves = -1
    steps = []
    while solution:
        steps.append(solution.state)
        moves += 1
        solution = solution.parent
    steps.reverse()

    return moves, steps
```

The `depth` function retrieves the depth of the tree node:
```python
def depth(self, node) -> int:
    depth = 0
    while node.parent is not None:
        node = node.parent
        depth += 1
    return depth   
```

The `timed_out` function is used on every algorithm, it checks if the current time exceeds 60 seconds, return true if so:
```python
def timed_out(self, before) -> bool:
    return time() - before > 60
```

The `show_graph` function opens a page on your browser with the visualization of the graph. The red nodes are part of the solution and the value of the nodes is of the type `depth: board`, where `depth` is the depthness on the graph and board is a flat state representation of the board.

The functions `search_heuristic_1`, `search_heuristic_2`, and `search_heuristic_3` are heuristics used to evaluate all states in informed search algorithms such as Greedy and A*. These heuristics provide estimates of the distance or cost to the goal from a given state in a search problem, and are used to guide the search algorithm towards the goal more efficiently by prioritizing promising states to explore first.

```python
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
```

#### BFS
This class contains the functions used to solve the puzzle with a classic bread-first search approach. Note that if there's a timeout while it is executing the algorithm, it stops and returns None. It's given the initial state of the board, as well as the win condition function and the operator function that obtains the childs states.
```python
def run(self, board, score : list):
    nodes = self.breadth_first_search(board, self.win, self.child_states)
    ...

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
```

#### DFS
This class contains the functions used to solve the puzzle with a classic depth-first search approach. Note that if there's a timeout while it is executing the algorithm, it stops and returns None. It's given the initial state of the board, as well as the win condition function and the operator function that obtains the childs states.
```python
def run(self, board : list, score : list):
    nodes = self.depth_first_search(board, self.win, self.child_states)

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
```

#### GREEDY
This class contains the functions used to solve the puzzle with a gready search approach. Note that if there's a timeout while it is executing the algorithm, it stops and returns None. It's given the initial state of the board, as well as the win condition function, the operator function that obtains the childs states as well as the heuristic to evaluate the board states:
```python
def run(self, board : list, score : list) -> None: # The result is stored in the score list
    nodes = self.greedy_search(board, self.win, self.child_states, self.search_heuristic_1)
    ...

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
            if child in filtered_states: continue
            
            filtered_states.append(child)
            # create tree node with the new state
            child_tree = TreeNode(child, node)
            node.add_child(child_tree)
            # enqueue the child node
            stack.append((child_tree, value))
        stack = sorted(stack, key = lambda node: node[1], reverse=True)
    return None
```

#### ASTAR

This class contains the functions used to solve the puzzle with the A* approach. Note that if there's a timeout while it is executing the algorithm, it stops and returns None. It's given the initial state of the board, as well as the win condition function, the operator function that obtains the childs states as well as the heuristic to evaluate the board states:
```python
def shortest_path(self, initial_coordinate, cluster):
    visited = set()
    queue = deque([(initial_coordinate, [])])

    while queue:
        (row, col), path = queue.popleft()
        if (row, col) in visited:continue
        visited.add((row, col))

        if cluster[row][col] == 1:return len(path)

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

def run(self, board : list, score : list) -> None:
    nodes = self.a_star_search(board, self.win, self.child_states, self.search_heuristic_2)

def a_star_search(self, initial_state, goal_state_func, operators_func, heuristic_func):
    root = TreeNode(initial_state)  # create the root node in the search tree
    stack = [(root, heuristic_func(initial_state))]  # initialize the queue to store the nodes
    filtered_states = [initial_state]

    while len(stack):

        if self.timed_out(self.before): return None

        node, _ = stack.pop()  # get first element in the queue
        if goal_state_func(node.state): return node

        children = operators_func(node.state)
        evaluated_children = [(child, heuristic_func(child) + self.depth(node) + 1) for child in children]

        for (child, value) in evaluated_children:  # go through next states
            if child in filtered_states:continue
            filtered_states.append(child)
            # create tree node with the new state
            child_tree = TreeNode(child, node)
            node.add_child(child_tree)
            # enqueue the child node
            stack.append((child_tree, value))
        stack = sorted(stack, key = lambda node: node[1], reverse=True)
    return None
```

---

This project was made possible by:

| Name | Email |
|-|-|
| Diogo Costa | up202007770@edu.fe.up.pt |
| Fábio Sá | up202007658@edu.fe.up.pt |
| João Araújo | up202004293@edu.fe.up.pt |
