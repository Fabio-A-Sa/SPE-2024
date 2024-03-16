"""
Auxiliar functions for the project.
"""

# Coordinate class
class Coordinate(object):
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    # Getter method for a Coordinate object's x coordinate.
    def getX(self) -> int:
        return self.x

    # Getter method for a Coordinate object's y coordinate
    def getY(self) -> int:
        return self.y

    # Verifies is the Coordinate object is inside the Recantangle Coordinates
    def is_inside_rect(self, coordinates : 'RectValue') -> bool:
        x1, y1, width, height = coordinates.getAllCoordinates()
        x1 -= width//2
        y1 -= height//2
        return self.x >= x1 and self.x <= x1 + width and self.y >= y1 and self.y <= y1 + height
    
    def __str__(self) -> str:
        return '<' + str(round(self.getX(), 0)) + ',' + str(round(self.getY(),0)) + '>'
    
    def __eq__(self, other) -> bool:
        return self.y == other.y and self.x == other.x
    
    def __neq__(self, other) -> bool:
        return self.y != other.y or self.x != other.x
    
    def __repr__(self) -> str:
        return "Coordinate(%d, %d)" % (self.x, self.y)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    
    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y)
        else:
            return Coordinate(self.x + other, self.y + other)
    
    def __sub__(self, other):
        try:
            if isinstance(other, Coordinate):
                return Coordinate(self.x - other.x, self.y - other.y)
            else:
                return Coordinate(self.x - other, self.y - other)
        except ValueError as e:
            raise ValueError("Negative coordinates given") from e

# ColorValue class
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

    # Getter method for a ColorValue object's r value.
    def getR(self) -> int:
        return self.r

    # Getter method for a ColorValue object's g value
    def getG(self) -> int:
        return self.g

    # Getter method for a ColorValue object's b value
    def getB(self) -> int:
        return self.b

    def __str__(self) -> str:
        return '(' + str(self.getR()) + ',' + str(self.getG()) + ',' + str(self.getB()) + ')'
    
    def __eq__(self, other) -> bool:
        return self.r == other.r and self.g == other.g and self.b == other.b
    
    def __repr__(self) -> str:
        return "ColorValue(%d, %d, %d)" % (self.r, self.g, self.b)
    
    def __len__(self):
        return 3 # Hard coded

    def __getitem__(self, key):
        return self.colour[key]

# Rectangle class
class RectValue(object):
    def __init__(self,x1,y1,width,height) -> None:
        try:
            self.coordinates = Coordinate(x1,y1)
            self.dimensions = Coordinate(width,height)
        except ValueError as e:
            raise ValueError("Invalid coordinates for Rectangle") from e
    
    # Getter method for a RectValue object's start coordinates.
    def getStartCoordinates(self) -> Coordinate:
        return self.coordinates.getX(), self.coordinates.getY(),
    
    # Getter method for a RectValue object's end coordinates.
    def getEndCoordinates(self) -> Coordinate:
        return self.dimensions.getX(), self.dimensions.getY()

    def getAllCoordinates(self) -> list:
        return self.coordinates.getX(), self.coordinates.getY(), self.dimensions.getX(), self.dimensions.getY()
    
    def __str__(self) -> str:
        return '<' + str(self.getStartCoordinates()) + ' | ' + str(self.getEndCoordinates()) + '>'
    
    def __eq__(self, other) -> bool:
        return self.coordinates == other.coordinates and self.dimensions == other.dimensions
    
    def __repr__(self) -> str:
        return "RectValue(%d, %d, %d, %d)" % (self.coordinates.x, self.coordinates.y, self.dimensions.x, self.dimensions.y)
    