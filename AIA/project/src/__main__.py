import c_draw as draw
from levels import LEVELS

'''
This is the entry point for the game.
It runs first the Main Menu, and only after selecting the level, does the game runs
'''
if __name__ == "__main__":
    while True:
        
        # Create the game main menu
        menu = draw.MainMenu(LEVELS)

        # Run the game main menu and get the level chosen by the player
        level = menu.run()

        if level == []: break

        # Create the game
        game = draw.Game(level)

        # Run the game, if the game is over, break the loop
        if game.run(): break
