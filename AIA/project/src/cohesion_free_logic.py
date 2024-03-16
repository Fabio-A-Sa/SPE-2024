
class Cohesion:
    '''
    This is a scrapped version of the game Cohesion Free. 
    The goal of the game is to connect all the same colored tiles together, which are called clusters. 
    The game's played on a symmetrical board (ex: 4x4). The player can click on a tile of a cluster and slide the cluster to any direction.
    The player can only slide a tile/cluster if there is an empty space on the destination tiles. 
    The player wins when there is only a single cluster of every color.
    '''

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

        self.side_dimension = len(self.board)
        self.game_over = False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.board))

    def get_board(self) -> list:
        return self.board

    def __check_piece_upwards(self, coords, cluster) -> bool:
        if coords[0] > 0:
            if self.board[coords[0] - 1][coords[1]] == self.board[coords[0]][coords[1]] and \
                    cluster[coords[0] - 1][coords[1]] == 0:
                cluster[coords[0] - 1][coords[1]] = 1
                self.__check_piece_upwards([coords[0] - 1, coords[1]], cluster)
                self.__check_piece_rightwards([coords[0] - 1, coords[1]], cluster)
                self.__check_piece_leftwards([coords[0] - 1, coords[1]], cluster)
        return False

    def __check_piece_downwards(self, coords, cluster) -> bool:
        if coords[0] < self.side_dimension - 1:
            if self.board[coords[0] + 1][coords[1]] == self.board[coords[0]][coords[1]] and \
                    cluster[coords[0] + 1][coords[1]] == 0:
                cluster[coords[0] + 1][coords[1]] = 1
                self.__check_piece_downwards([coords[0] + 1, coords[1]], cluster)
                self.__check_piece_rightwards([coords[0] + 1, coords[1]], cluster)
                self.__check_piece_leftwards([coords[0] + 1, coords[1]], cluster)
        return False

    def __check_piece_rightwards(self, coords, cluster) -> bool:
        if coords[1] < self.side_dimension - 1:
            if self.board[coords[0]][coords[1] + 1] == self.board[coords[0]][coords[1]] and \
                    cluster[coords[0]][coords[1] + 1] == 0:
                cluster[coords[0]][coords[1] + 1] = 1
                self.__check_piece_rightwards([coords[0], coords[1] + 1], cluster)
                self.__check_piece_downwards([coords[0], coords[1] + 1], cluster)
                self.__check_piece_upwards([coords[0], coords[1] + 1], cluster)
        return False

    def __check_piece_leftwards(self, coords, cluster) -> bool:
        if coords[1] > 0:
            if self.board[coords[0]][coords[1] - 1] == self.board[coords[0]][coords[1]] and \
                    cluster[coords[0]][coords[1] - 1] == 0:
                cluster[coords[0]][coords[1] - 1] = 1
                self.__check_piece_leftwards([coords[0], coords[1] - 1], cluster)
                self.__check_piece_downwards([coords[0], coords[1] - 1], cluster)
                self.__check_piece_upwards([coords[0], coords[1] - 1], cluster)
        return False

    def __get_cluster(self, coords) -> list:
        if self.board[coords[0]][coords[1]] == None:
            return []
        cluster = [[0 for _ in range(self.side_dimension)] for _ in range(self.side_dimension)]
        cluster[coords[0]][coords[1]] = 1
        self.__check_piece_upwards(coords, cluster)
        self.__check_piece_downwards(coords, cluster)
        self.__check_piece_rightwards(coords, cluster)
        self.__check_piece_leftwards(coords, cluster)
        return cluster

    def move(self, coords : list, direction) -> int:
        cluster = self.__get_cluster(coords)
        if cluster == []:
            return 0
        
        color = self.board[coords[0]][coords[1]]
        
        new_board = [[element for element in row] for row in self.board]

        # Remove the cluster from the board
        for i in range(0, self.side_dimension):
            for j in range(0, self.side_dimension):
                if cluster[i][j] == 1:
                    new_board[i][j] = None

        if direction == "up":
            for i in range(0, self.side_dimension - 1):
                if cluster[0][i] == 1:
                    return 0

            for i in range(0, self.side_dimension - 1):
                for j in range(0, self.side_dimension):
                    cluster[i][j] = cluster[i + 1][j]
            for i in range(0, self.side_dimension):
                cluster[self.side_dimension - 1][i] = 0

        elif direction == "down":
            for i in range(0, self.side_dimension):
                if cluster[self.side_dimension - 1][i] == 1:
                    return 0
            for i in range(self.side_dimension - 1, -1, -1):
                for j in range(0, self.side_dimension):
                    cluster[i][j] = cluster[i - 1][j]
            for i in range(0, self.side_dimension):
                cluster[0][i] = 0

        elif direction == "left":
            for i in range(0, self.side_dimension):
                if cluster[i][0] == 1:
                    return 0
            for i in range(0, self.side_dimension):
                for j in range(0, self.side_dimension - 1):
                    cluster[i][j] = cluster[i][j + 1]
            for i in range(0, self.side_dimension):
                cluster[i][self.side_dimension - 1] = 0

        elif direction == "right":
            for i in range(0, self.side_dimension):
                if cluster[i][self.side_dimension - 1] == 1:
                    return 0
            for i in range(0, self.side_dimension):
                for j in range(self.side_dimension - 1, -1, -1):
                    cluster[i][j] = cluster[i][j - 1]
            for i in range(0, self.side_dimension):
                cluster[i][0] = 0

        for i in range(0, self.side_dimension):
            for j in range(0, self.side_dimension):
                if cluster[i][j] == 1:
                    if new_board[i][j] == None:
                        new_board[i][j] = color
                    else:
                        return 0
                    
        self.board = new_board

        return 1

    # returns True if the game is over, False otherwise
    def win_condition(self) -> bool:

        clusters_to_see = [(i, j) for i in range(self.side_dimension) for j in range(self.side_dimension)]

        aux_colors = {
            'r': 0,
            'b': 0,
            'g': 0,
            'y': 0,
        }

        for (i, j) in clusters_to_see:
            cluster = self.__get_cluster([i, j])
            if cluster == []:
                continue
            aux_colors[self.board[i][j]] = 0
            for p in range(0, self.side_dimension):
                for q in range(0, self.side_dimension):
                    if cluster[p][q] == 1:
                        clusters_to_see.remove((p, q))
                        aux_colors[self.board[p][q]] += 1

        if aux_colors == self.colors:
            self.game_over = True
            return True
        else:
            return False

    def __str__(self) -> str:
        string = "Board: \n"
        for i in range(1, self.side_dimension + 1):
            string += str(self.board[i - 1]) + "\n"
        return string

