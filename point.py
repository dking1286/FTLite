## Point class for FTLite ##
import math

class Point(object):
    """Represents a point in a two dimensional plane
    attributes:
        _x (int)
        _y (int)
        x  (int, property)
        y  (int, property)
    instance methods:
        Point( int x, int y )
        operator+( Point p1, Point p2 )
        operator-( Point p1, Point p2 )
        coords()
        distanceTo( Point other )
    """
    def __init__( self, x, y ):
        if type(x) is not int or type(y) is not int:
            raise TypeError('A Point object must have integer coordinates')
        
        self.x = x
        self.y = y
    
    def __add__( self, other ):
        """Add points componentwise"""
        return Point( self._x + other._x, self._y + other._y )
        
    def __sub__( self, other ):
        """Subtract points componentwise"""
        return Point( self._x - other._x, self._y - other._y )
    
    def coords( self ):
        """Returns a 2-tuple of the x and y coordinates"""
        return self.x, self.y
    
    def distanceTo( self, other ):
        """Returns a float representing the distance to another point"""
        return math.sqrt( (self.x - other.x)**2 + (self.y - other.y)**2 )
    
    @property
    def x( self ):
        return self._x
    
    @x.setter
    def x( self, newX ):
        self._x = newX
    
    @property
    def y( self ):
        return self._y
    
    @y.setter
    def y( self, newY ):
        self._y = newY
    
