from c_display import Display
from c_auxiliar_functions import Coordinate, ColorValue, RectValue
from c_algorithms import *
from cohesion_free_logic import Cohesion
from threading import Thread
from copy import deepcopy

BLACK = ColorValue(0, 0, 0)
WHITE = ColorValue(255, 255, 255)
RED = ColorValue(255, 0, 0)
GREEN = ColorValue(0, 255, 0)
BLUE = ColorValue(0, 0, 255)
YELLOW = ColorValue(255, 255, 0)
LIGHT_GREY = ColorValue(216, 216, 216)

# Board colors
COLORS = {
    'r': RED,
    'g': GREEN,
    'b': BLUE,
    'y': YELLOW,
    None: WHITE
}

'''
This MutualDrawFunctions Class contains the common functions to be used in both the Main Menu and the Game itself.
Draws the background with a changing gradient, and a Grey rectangle, where the content is displayed.
'''
class MutualDrawFunctions:

    def __init__(self) -> None:
        # Get the display
        self.display = Display()

        # Get the events to be used
        self.quit_event = self.display.get_quit_event()
        self.mouse_button_down = self.display.get_mouse_button_down_event()
        self.mouse_button_up = self.display.get_mouse_button_up_event()

        # Set the center position of the screen
        self.center_position = self.instructions_button_position = Coordinate(self.display.get_width() / 2, self.display.get_height() / 2)

        # Set the position of the back button outside the content rectangle
        self.back_button_position = Coordinate(self.display.get_width() / 7, self.display.get_height() / 8 )

        # Set the running boolean to the default value, assuring there is something running 
        self.running = True

        # Default background gradient values
        self.HUE_OFFSET = 0
        self.HUE_CHANGE_SPEED = 0.5 # This value can be changed to update the speed of the background color changing

        # Set the position of the content rectangle
        self.content_rectangle = RectValue(self.display.get_width() / 10, self.display.get_height() / 5, 
                                           self.display.get_width() / 1.11 - self.display.get_width() / 10, self.display.get_height() / 1.11 - self.display.get_height() / 7)

    def draw_background(self) -> None:

        # Clear the screen
        self.display.fill(WHITE)

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

        # Draw a border for the content
        self.display.draw_rect(BLACK, self.content_rectangle, 5)

    # Stops running the program and closes the display
    def quit(self):
        self.running = False
        self.display.quit()

'''
The MainMenu Class contains the mutual drawing functions of the MutualDrawFunctions Class.
Draws the menu entry point, the instructions, and the level selection.
'''
class MainMenu(MutualDrawFunctions):

    def __init__(self, levels : dict) -> None:
        super().__init__()
        
        # Set the position of the items on the screen
        self.menu_name_position = Coordinate(self.display.get_width() / 2, self.display.get_height() / 8)
        self.play_button_position = Coordinate(self.display.get_width() / 2, self.display.get_height() / 3)
        self.instructions_button_position = self.center_position
        self.quit_button_position = Coordinate(self.display.get_width() / 2, self.display.get_height() / 1.5 )
        self.instructions_text_position = Coordinate(self.display.get_width() / 2, self.display.get_height() / 4)


        # Set the default boolean values for the current position on the main menu
        self.running_menu = True
        self.running_instructions = False
        self.running_level_selection = False

        # Set the default hovering values to false
        self.hovering_play = False
        self.hovering_instructions = False
        self.hovering_quit = False
        self.hovering_menu = False

        # Set the Columns for each level difficulty
        self.level_easy_column = Coordinate(self.display.get_width() / 5, self.display.get_height() / 4 )
        self.level_medium_column = Coordinate(self.display.get_width() / 2, self.display.get_height() / 4 )
        self.level_hard_column = Coordinate(self.display.get_width() / 1.25, self.display.get_height() / 4 )

        # Set the spacing between levels
        self.level_spacing = 90

        # Set the levels
        self.levels = levels

        # Limits the placement of the levels on the screen to a maximum of 15
        self.MAX_LEVELS = 15

        # Hovering level dictionaire defaulted to False
        self.hovering_level = {}

        for i in range(self.MAX_LEVELS):
            self.hovering_level[i] = False

        # Set the instructions text
        self.instructions_text =[
            "The game Cohesion is a one-player game played on a pre-generated board with up to four different colors.",
            "The game starts with a scrambled board, and the player must slide tiles to form",
            "the largest clusters of tiles of the same color.",
            "The game ends when the player wins by having only 1 cluster of each color",
            "or when the player can no longer make any moves, in which case he has lost.",
            "",
            "If you want help to solve the puzzle, press on a algorithm name at any state of the puzzle.",
            "The name becomes a fixed red after pressing it. After getting a solution you can move through the board states.",
            "If you want to reset the board and the time, press the Reset button. It doesn't reset the algorithms solutions.",
            "After running an algorithm, you can see its graph by pressing the Show Graph button.",
            "The win condition is only obtained by the moves the player makes, algorithm ones doesn't count."]

    def run(self) -> list:

        while self.running:
            for event in self.display.get_events():

                # Quits the game if it receives a quit event
                if event.type == self.quit_event:
                    self.quit()
                    return []
                elif event.type == self.mouse_button_up:
                    # Changes the screen to the level selection
                    if self.hovering_play: 
                        self.hovering_play = False
                        self.running_instructions = False
                        self.running_menu = False
                        self.running_level_selection = True

                    # Changes the screen to the instructions menu
                    elif self.hovering_instructions:
                        self.hovering_instructions = False
                        self.running_instructions = True
                        self.running_menu = False

                    # Changes the screen to the main menu
                    elif self.hovering_menu:
                        self.hovering_menu = False
                        self.running_instructions = False
                        self.running_level_selection = False
                        self.running_menu = True

                    # Quits the main menu if the quit button was pressed
                    elif self.hovering_quit:
                        self.quit()
                        return []
                    for i, level in enumerate(self.levels, start=0):
                        if i >= self.MAX_LEVELS: break

                        # If the level was pressed, close the main menu and return the level selected
                        if self.hovering_level[i]:
                            self.hovering_level[i] = False
                            self.running_instructions = False
                            self.running_menu = False
                            self.running_level_selection = False
                            self.running_level_selection = True

                            self.quit()
                            return self.levels[level]

            self.draw()
            self.display.update()

    def draw(self) -> None:
        
        self.draw_background()

        self.display.draw_text_centered("Cohesion Free", BLACK, self.menu_name_position, "Bigger")

        if self.running_menu:
            self.__draw_main_menu()
        elif self.running_instructions:
            self.__draw_intructions()
        elif self.running_level_selection:
            self.__draw_level_selection()

    def __draw_main_menu(self) -> None:
        mouse_pos = self.display.get_mouse_pos()

        if mouse_pos.is_inside_rect(RectValue(self.play_button_position.getX(), self.play_button_position.getY(), 100, 50)):
            self.display.draw_text_centered("Play", RED, self.play_button_position, "Normal")
            self.hovering_play = True
        else:  
            self.display.draw_text_centered("Play", BLACK, self.play_button_position, "Normal")
            self.hovering_play = False

        if mouse_pos.is_inside_rect(RectValue(self.instructions_button_position.getX(), self.instructions_button_position.getY(), 220, 50)):
            self.display.draw_text_centered("Instructions", RED, self.instructions_button_position, "Normal")
            self.hovering_instructions = True
        else:  
            self.display.draw_text_centered("Instructions", BLACK, self.instructions_button_position, "Normal")
            self.hovering_instructions = False

        if mouse_pos.is_inside_rect(RectValue(self.quit_button_position.getX(), self.quit_button_position.getY(), 100, 50)):
            self.display.draw_text_centered("Quit", RED, self.quit_button_position, "Normal")
            self.hovering_quit = True
        else:  
            self.display.draw_text_centered("Quit", BLACK, self.quit_button_position, "Normal")
            self.hovering_quit = False

    def __draw_intructions(self) -> None:
        mouse_pos = self.display.get_mouse_pos()

        for i, line in enumerate(self.instructions_text):
            self.display.draw_text_centered(line, BLACK, self.instructions_text_position + Coordinate(0, i*35) , "Smaller")
        
        self.display.draw_rect_centered(BLACK, RectValue(self.back_button_position.getX(), self.back_button_position.getY(), 100, 50), Coordinate(100,50))

        if mouse_pos.is_inside_rect(RectValue(self.back_button_position.getX(), self.back_button_position.getY(), 100, 50)):
            self.display.draw_text_centered("Back", RED, self.back_button_position, "Normal")
            self.hovering_menu = True
        else:  
            self.display.draw_text_centered("Back", WHITE, self.back_button_position, "Normal")
            self.hovering_menu = False

    def __draw_level_selection(self) -> None:
        mouse_pos = self.display.get_mouse_pos()

        self.display.draw_rect_centered(BLACK, RectValue(self.back_button_position.getX(), self.back_button_position.getY(), 100, 50), Coordinate(100,50))


        for i, level in enumerate(self.levels, start=0):
            if i == self.MAX_LEVELS: break

            self.display.draw_text_centered("Easy", BLACK, self.level_easy_column, "Normal")
            self.display.draw_text_centered("Normal", BLACK, self.level_medium_column, "Normal")
            self.display.draw_text_centered("Hard", BLACK, self.level_hard_column, "Normal")
            
            if i//5 == 0: column = self.level_easy_column
            elif i//5 == 1: column = self.level_medium_column
            elif i//5 == 2: column = self.level_hard_column
            
            if mouse_pos.is_inside_rect(RectValue(column.getX(), column.getY() + (i%5+1)*self.level_spacing, 75, 75)):
                self.display.draw_text_centered(str(level), RED, column + Coordinate(0, (i%5+1)*self.level_spacing) , "Smaller")
                self.hovering_level[i] = True
            else:
                self.display.draw_text_centered(str(level), BLACK, column + Coordinate(0, (i%5+1)*self.level_spacing) , "Smaller")
                self.hovering_level[i] = False
                
            self.__draw_board(self.levels[level], column + Coordinate(75, (i%5+1)*self.level_spacing))

        if mouse_pos.is_inside_rect(RectValue(self.back_button_position.getX(), self.back_button_position.getY(), 100, 50)):
            self.display.draw_text_centered("Back", RED, self.back_button_position, "Normal")
            self.hovering_menu = True
        else:  
            self.display.draw_text_centered("Back", WHITE, self.back_button_position, "Normal")
            self.hovering_menu = False
    
    def __draw_board(self, board, position) -> None:
        board_size = 50
        cell_size = board_size // len(board)
        displacement = Coordinate(board_size, board_size)
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                color = COLORS[cell]
                self.display.draw_rect_centered(color, RectValue(position.getX() + j*cell_size, position.getY() + i*cell_size, cell_size, cell_size),displacement)

        self.display.draw_rect_centered(BLACK, RectValue(position.getX(), position.getY()-1, board_size, board_size),displacement, width=2)

# Game Draw Class
'''
The Game Class contains the mutual drawing functions of the MutualDrawFunctions Class.
Draws the board itself and the solving algorithms to help the player.
'''
class Game(MutualDrawFunctions):

    def __init__(self, board) -> None:
        super().__init__()

        # Set the incoming board as the level
        self.game = Cohesion(board)

        # Sets the board
        self.board = board

        # In case of a level reset, need to copy the board.
        self.initial_board = deepcopy(board)
        self.board_size = len(self.board)
        
        # Set the default position on the screen
        self.board_position = Coordinate(self.display.get_width() / 2, self.display.get_height() / 1.7)
        self.algorithms_position = Coordinate(self.display.get_width() / 1.35, self.display.get_height() / 3.5)
        self.moves_position = Coordinate(self.display.get_width() / 8, self.display.get_height() / 3.5)
        self.time_position = Coordinate(self.display.get_width() / 8, self.display.get_height() / 2.5)
        self.reset_button_position = Coordinate(self.display.get_width() / 6, self.display.get_height() / 1.25)

        self.win_text_position = Coordinate(self.display.get_width() / 2, self.display.get_height() / 4)

        # Set the spacing between solving algorithms
        self.algorithm_spacing = 120

        self.hovering_menu = False

        # Local auxiliar values
        moves = 0
        time = 0
        executed = False
        graph_executed = False
        finished = False
        moves_list = []

        # Set the algorithm list
        # It stores the name of the algorithm, as well as a list of atributes to be manipulated by the algorithm threads, when running
        self.algorithms = {
            "BFS": [BFS(),[time,moves, executed, moves_list, finished, graph_executed]],
            "DFS": [DFS(),[time,moves, executed, moves_list, finished, graph_executed]],
            "Greedy": [GREEDY(),[time,moves, executed, moves_list, finished, graph_executed]],
            "A*": [ASTAR(),[time,moves, executed, moves_list, finished, graph_executed]],
        }

        self.hovering_algorithm = [False for _ in range(len(self.algorithms))]
        self.hovering_show_graph_button = [False for _ in range(len(self.algorithms))]
        self.hovering_less_button = [False for _ in range(len(self.algorithms))]
        self.hovering_greater_button = [False for _ in range(len(self.algorithms))]
        self.hovering_reset = False
        self.current_move = [0 for _ in range(len(self.algorithms))]
        self.time = self.display.get_time()

        self.board_width = 400
        self.cell_size = self.board_width // len(self.board)
        self.displacement = Coordinate(self.board_width, self.board_width)

        self.initial_cell_position = self.board_position - Coordinate(self.board_width//2, self.board_width//2)

        self.win_condition_obtained = False

        self.moves = 0  # Number of moves made by the player

        # Sets an outside cell to notice the player it didn't select a correct cell
        self.wrong_cell = (-2,-2)


    # Returns True if the game is over, False if the player went back to the main menu
    def run(self) -> bool:
        while self.running:
            self.mouse_pos = self.display.get_mouse_pos()

            if not self.win_condition_obtained:
                self.time += self.display.get_time()

            for event in self.display.get_events():
                if event.type == self.quit_event:
                    self.quit()
                    return True
                
                elif event.type == self.mouse_button_down:
                    for i, row in enumerate(self.board):
                        for j, _ in enumerate(row):
                            if self.mouse_pos.is_inside_rect(RectValue(self.initial_cell_position.getX() + (j+0.5)*self.cell_size, self.initial_cell_position.getY() + (i+0.5)*self.cell_size, self.cell_size, self.cell_size)):
                                if(self.board[i][j]): # If the player clicks on a cell that is not empty
                                    self.pressed_cell = (i,j)
                                else:
                                    self.pressed_cell = self.wrong_cell 

                elif event.type == self.mouse_button_up:
                    if self.hovering_menu: 
                        self.quit()
                        return False
                    
                    elif self.hovering_reset:
                        self.board = self.initial_board
                        self.game = Cohesion(self.board)
                        self.win_condition_obtained = False
                        for i, _ in enumerate(self.algorithms):
                            self.current_move[i] = 0
                        self.moves = 0
                        self.time = 0
                    
                    else:
                        for i, algorithm in enumerate(self.algorithms):
                            # If the player clicks on an algorithm, invokes the algorithm on a new Thread
                            # If the algorithm is already running, it won't be invoked again
                            if self.hovering_algorithm[i] and not self.algorithms[algorithm][1][2]:
                                self.algorithms[algorithm][1][2] = True
                                x = Thread(target=self.algorithms[algorithm][0].run, args=(self.board, self.algorithms[algorithm][1],))
                                x.start()
                                break

                            # If the player clicks on the less button, goes to the previous board state
                            elif self.hovering_less_button[i] and self.current_move[i] > 0:
                                self.current_move[i] -= 1
                                self.board = self.algorithms[algorithm][1][3][self.current_move[i]]
                                for j, _ in enumerate(self.algorithms):
                                    if j != i:
                                        self.current_move[j] = 0
                                break

                            # If the player clicks on the greater button, goes to the next board state
                            elif self.hovering_greater_button[i] and self.current_move[i] < self.algorithms[algorithm][1][1] :
                                self.current_move[i] += 1
                                self.board = self.algorithms[algorithm][1][3][self.current_move[i]]
                                for j, _ in enumerate(self.algorithms):
                                    if j != i:
                                        self.current_move[j] = 0
                                break

                            # If the player clicks on the show graph button, shows the graph of the algorithm
                            elif self.hovering_show_graph_button[i] and not self.algorithms[algorithm][1][4]:
                                x = Thread(target=self.algorithms[algorithm][0].show_graph)
                                x.start()
                                self.algorithms[algorithm][1][4] = True         
                                break                   
                    
                        if not self.win_condition_obtained:
                            for i, row in enumerate(self.board):
                                for j, _ in enumerate(row):
                                    if self.mouse_pos.is_inside_rect(RectValue(self.initial_cell_position.getX() + (j+0.5)*self.cell_size, self.initial_cell_position.getY() + (i+0.5)*self.cell_size, self.cell_size, self.cell_size)):
                                        self.unpressed_cell = (i,j)

                                        if self.pressed_cell[0] == self.unpressed_cell[0] and self.pressed_cell[1] == self.unpressed_cell[1]:
                                            direction = None
                                        elif self.pressed_cell[0] < 0 and self.pressed_cell[1] < 0:
                                            direction = None
                                        elif self.pressed_cell[0] < self.unpressed_cell[0]:
                                            direction = "down"
                                        elif self.pressed_cell[0] > self.unpressed_cell[0]:
                                            direction = "up"
                                        elif self.pressed_cell[1] < self.unpressed_cell[1]:
                                            direction = "right"
                                        elif self.pressed_cell[1] > self.unpressed_cell[1]:
                                            direction = "left"
                                        else:
                                            direction = None

                                        if direction:
                                            self.moves += self.game.move(self.pressed_cell, direction)
                                            self.board = self.game.get_board()
                                            self.win_condition_obtained = self.game.win_condition()
                                        
                                        self.pressed_cell = self.wrong_cell 
                                        break
       
            self.draw()
            self.display.update()

    def draw(self) -> None:
        self.draw_background()
        self.__draw_board()
        self.__draw_algorithms()
        self.__draw_score()

        self.display.draw_rect_centered(BLACK, RectValue(self.back_button_position.getX(), self.back_button_position.getY(), 100, 50), Coordinate(100,50))

        if self.mouse_pos.is_inside_rect(RectValue(self.back_button_position.getX(), self.back_button_position.getY(), 100, 50)):
            self.display.draw_text_centered("Back", RED, self.back_button_position, "Normal")
            self.hovering_menu = True
        else:  
            self.display.draw_text_centered("Back", WHITE, self.back_button_position, "Normal")
            self.hovering_menu = False
    
    def __draw_board(self) -> None:

        # Draw the board
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                color = COLORS[cell]
                self.display.draw_rect_centered(color, RectValue(self.board_position.getX() + j*self.cell_size, self.board_position.getY() + i*self.cell_size, self.cell_size, self.cell_size),self.displacement)

        # Draw the outside grid
        self.display.draw_rect_centered(BLACK, RectValue(self.board_position.getX(), self.board_position.getY(), self.board_width, self.board_width), self.displacement, 2)

        for i in range(self.board_size):
            for j in range(self.board_size):
                start_down_coordinates = self.initial_cell_position + Coordinate((i+1)*self.cell_size, j*self.cell_size)
                start_right_coordinates = self.initial_cell_position + Coordinate(i*self.cell_size, (j+1)*self.cell_size)
                end_coordinates = self.initial_cell_position + Coordinate((i+1)*self.cell_size, (j+1)*self.cell_size)
                self.display.draw_line(BLACK, start_down_coordinates, end_coordinates, 1)
                self.display.draw_line(BLACK, start_right_coordinates, end_coordinates, 1)

    def __draw_score(self) -> None:

        # Draw the current number of moves and time
        self.display.draw_text("Moves: " + str(self.moves), BLACK, self.moves_position, "Normal")
        self.display.draw_text("Time: " + str(round(self.time, 2)), BLACK, self.time_position, "Normal")

        if self.win_condition_obtained:
            self.display.draw_text_centered("Puzzle Solved!", RED, self.win_text_position, "Normal")

        # Draw the reset button
        if self.mouse_pos.is_inside_rect(RectValue(self.reset_button_position.getX(), self.reset_button_position.getY(), 100, 50)):
            self.display.draw_text_centered("Reset", RED, self.reset_button_position, "Normal")
            self.hovering_reset = True
        else:
            self.display.draw_text_centered("Reset", BLACK, self.reset_button_position, "Normal")
            self.hovering_reset = False

    # Draw the algorithms
    def __draw_algorithms(self) -> None:
        for i, algorithm in enumerate(self.algorithms):
            algorithm_position = self.algorithms_position + Coordinate(0, i*self.algorithm_spacing)
            if self.mouse_pos.is_inside_rect(RectValue(algorithm_position.getX(), algorithm_position.getY(), 75, 75)) or self.algorithms[algorithm][1][2]:
                self.display.draw_text_centered(algorithm, RED, algorithm_position, "Smaller")
                self.hovering_algorithm[i] = True
            else:
                self.display.draw_text_centered(algorithm, BLACK, algorithm_position, "Smaller")
                self.hovering_algorithm[i] = False

            if self.algorithms[algorithm][1][5]: # Show graph button only if the algorithm has run
                if self.mouse_pos.is_inside_rect(RectValue(algorithm_position.getX()+120, algorithm_position.getY(), 120, 25)) or self.algorithms[algorithm][1][4]:
                    self.display.draw_text_centered("Show Graph", RED, algorithm_position + Coordinate(120, 0), "Smaller")
                    self.hovering_show_graph_button[i] = True
                else:
                    self.display.draw_text_centered("Show Graph", BLACK, algorithm_position + Coordinate(120,0), "Smaller")
                    self.hovering_show_graph_button[i] = False

                # Draw the algorithm's buttons
                less_button_position = algorithm_position + Coordinate(120, 30)
                greater_button_position = algorithm_position + Coordinate(180, 30)

                if self.mouse_pos.is_inside_rect(RectValue(less_button_position.getX(), less_button_position.getY(), 20, 20)):
                    self.display.draw_text_centered("<", RED, less_button_position, "Smaller")
                    self.hovering_less_button[i] = True
                else:
                    self.display.draw_text_centered("<", BLACK, less_button_position, "Smaller")
                    self.hovering_less_button[i] = False
                
                if self.mouse_pos.is_inside_rect(RectValue(greater_button_position.getX(), greater_button_position.getY(), 20, 20)):
                    self.display.draw_text_centered(">", RED, greater_button_position, "Smaller")
                    self.hovering_greater_button[i] = True
                else:
                    self.display.draw_text_centered(">", BLACK, greater_button_position, "Smaller")
                    self.hovering_greater_button[i] = False

                self.display.draw_text_centered(str(self.current_move[i]), BLACK, algorithm_position + Coordinate(150,30), "Smaller")
            
            # Draw the algorithm's Time and Moves
            self.display.draw_text("Time: " + str(self.algorithms[algorithm][1][0]), BLACK, algorithm_position + Coordinate(0, 15), "Smaller")
            self.display.draw_text("Moves: " + str(self.algorithms[algorithm][1][1]), BLACK, algorithm_position + Coordinate(0, 40), "Smaller")