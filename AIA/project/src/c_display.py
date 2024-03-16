import pygame
from c_auxiliar_functions import Coordinate, ColorValue, RectValue

BLACK = ColorValue(0, 0, 0)

# Display class
class Display(object):

    def __init__(self, width : int = 1280, height : int = 720) -> None:

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

    # Update the display
    def update(self) -> None:
        pygame.display.update()
        self.clock.tick(self.fps)

    # Fill the screen with a color
    def fill(self, color : ColorValue = BLACK) -> None:
        self.screen.fill(color.color)

    # Draw text centered on a point of the screen
    def draw_text_centered(self, text : str, color : ColorValue = BLACK, pos : Coordinate = Coordinate(0,0), font : str = "Normal") -> None:
        
        # Set the font
        if font == "Normal":
            f = self.normal_font
        elif font == "Bigger":
            f = self.bigger_font
        elif font == "Smaller":
            f = self.smaller_font
        else:
            f = self.normal_font
        
        # Render the text
        text_surface = f.render(text, True, color.color)

        # Get the size of the text surface
        text_width, text_height = text_surface.get_size()

        # Calculate the position of the text surface
        text_x = pos.getX() - (text_width // 2)
        text_y = pos.getY() - (text_height // 2)

        # Create the new coordinates for the text surface
        text_rect = Coordinate(text_x, text_y)

        self.blit(text_surface, text_rect)

    # Draw text on the screen
    def draw_text(self, text : str, color : ColorValue = BLACK, pos : Coordinate = Coordinate(0,0), font : str = "Normal") -> None:

        # Set the font
        if font == "Normal": f = self.normal_font
        elif font == "Bigger": f = self.bigger_font
        elif font == "Smaller": f = self.smaller_font
        else: f = self.normal_font

        text_surface = f.render(text, True, color.color)
        self.blit(text_surface, pos)

    # Blit a surface on the screen
    def blit(self, surface: pygame.Surface, pos : Coordinate = Coordinate(0,0)) -> None:
        self.screen.blit(surface, (pos.getX(), pos.getY()))

    # Draw a rectangle centered on a point of the screen
    def draw_rect_centered(self, color: ColorValue = BLACK, rect : RectValue = RectValue(0,0,0,0), displacement : Coordinate = Coordinate(0,0),  width : int = 0) -> None:
        x, y, w, h = rect.getAllCoordinates()
        
        # Calculate the position of the rectangle
        if displacement.getX() != 0 or displacement.getY() != 0:
            rect_x = x - (displacement.getX() // 2)
            rect_y = y - (displacement.getY() // 2)
        else:
            rect_x = x - (w // 2)
            rect_y = y - (h // 2)

        # Create the new coordinates for the rectangle
        rect = RectValue(rect_x, rect_y, w, h)
        pygame.draw.rect(self.screen, color.color, rect.getAllCoordinates(), width)

    # Draw a rectangle on the screen
    def draw_rect(self, color: ColorValue = BLACK, rect : RectValue = RectValue(0,0,0,0),  width : int = 0) -> None:
        pygame.draw.rect(self.screen, color.color, rect.getAllCoordinates(), width)
    
    # Draw a line on the screen
    def draw_line(self, color: ColorValue = BLACK, start_pos : Coordinate = Coordinate(0,0), end_pos : Coordinate = Coordinate(0,0), width : int = 1) -> None:
        pygame.draw.line(self.screen, color.color, (start_pos.getX(), start_pos.getY()), (end_pos.getX(), end_pos.getY()), width)

    # Draw a line on the screen
    def draw_standart_line(self, color: pygame.color, start_pos : Coordinate = Coordinate(0,0), end_pos : Coordinate = Coordinate(0,0), width : int = 1) -> None: 
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

    # Get the width of the display
    def get_width(self) -> int:
        return self.width

    # Get the height of the display
    def get_height(self) -> int:
        return self.height
    
    # Get the center of the display
    def get_center(self) -> Coordinate:
        return Coordinate(self.width / 2, self.height / 2)

    # Get the FPS of the display
    def get_fps(self) -> int:
        return self.fps

    # Get the current time in seconds
    def get_time(self) -> float:
        return self.clock.get_time() / 1000

    # Get the clock
    def get_clock(self) -> pygame.time.Clock:
        return self.clock

    # Get the screen
    def get_screen(self) -> pygame.Surface:
        return self.screen
    
    # Get the pygame color
    def get_color_object(self) -> pygame.color.Color:
        return pygame.color.Color(0,0,0)

    # Get the events
    def get_events(self) -> list:
        return pygame.event.get()
    
    # Get the mouse position
    def get_mouse_pos(self) -> Coordinate:
        x, y = pygame.mouse.get_pos()
        return Coordinate(x, y)
    
    # Get the mouse button down
    def get_mouse_button_down_event(self) -> int:
        return pygame.MOUSEBUTTONDOWN

    # Get the mouse button up
    def get_mouse_button_up_event(self) -> int:
        return pygame.MOUSEBUTTONUP

    # Get the quit event
    def get_quit_event(self) -> int:
        return pygame.QUIT
    
    # Quit the game
    def quit(self) -> None:
        pygame.quit()
