## User Interface for FTLite ##
import tkinter as tk

import constants
from point import Point
from task import Task
from decorators import returnFunc
import weapons

class UserInterface(object):
    """Represents the buttons, displays, and other components of the
    user interface available to the player
    attributes:
        battle (Battle)
        canvas (tk.Canvas)
        playerShipImage (image&)
        enemyShipImage (image&)
        playerHullBar (Bar)
        enemyHullBar (Bar)
    instance methods:
        UserInterface( battle )
        update()
        onGameOver()
        makeButton( x, y, command=None, text=None )
        itemConfigure( item, options ) {@returnFunc}
        moveShot( shot, dx, dy ) {@returnFunc}
    """
    def __init__(self, battle):
        self.battle = battle
        
        # Initialize the canvas
        self.canvas = tk.Canvas( self.battle.root,
                                 height=constants.canvasHeight,
                                 width=constants.canvasWidth,
                                 background='#FFFFFF' )
        self.canvas.grid()
        
        # Place ship images on the canvas
        self.playerShipImage = self.canvas.create_image( *constants.playerShipLocation.coords(),
                                                         image=self.battle.playerShip.image )
        self.enemyShipImage = self.canvas.create_image(  *constants.enemyShipLocation.coords(),
                                                         image=self.battle.enemyShip.image )

        # Place display bars on canvas
        self.playerHullBar = Bar( self, corner=constants.playerHullDisplayCorner )
        self.enemyHullBar = Bar( self, corner=constants.enemyHullDisplayCorner )
        
        # Test buttons and other items
        self.fireLaserButton = self.makeButton( *constants.fireLaserButtonLocation.coords(),
                                                command=self.onFireLaserButtonClick,
                                                text='Fire laser' )
        self.fireMissileButton = self.makeButton( *constants.fireMissileButtonLocation.coords(),
                                                  command=self.onFireMissileButtonClick,
                                                  text='Fire missile' )
    
    def update( self ):
        """Updates the appearance of the bars and other items
        
        Called at 60 FPS in the battle._animate methods
        """
        self.playerHullBar.update( self.battle.playerShip.hull )
        self.enemyHullBar.update( self.battle.enemyShip.hull )
    
    def onGameOver( self ):
        pass
    
    def makeButton( self, x, y, command=None, text=None ):
        """Creates and places a button on the canvas
        args:
            x (int)
            y (int)
            command (function)
            text (str)
        returns: a reference to the button that was created
        """
        if command == None:
            raise TypeError('A button must have an associated function')
        
        ref = tk.Button( self.battle.root, command=command, text=text )
        self.canvas.create_window( x, y, window=ref )
        return ref
    
    @returnFunc
    def itemConfigure( self, item, **kwargs ):
        """Configures the properties of an item on the canvas
        args:
            item (&item): A reference to the item being configured
            **kwargs: The properties of the item that should be configured
        """
        self.canvas.itemconfigure( item, **kwargs )
    
    @returnFunc
    def moveShot( self, shot, dx, dy ):
        """Moves a shot on the canvas
        args:
            shot (&image)
            dx (int)
            dy (int)
        """
        self.canvas.move( shot, dx, dy )
    
    def onFireLaserButtonClick( self ):
        """Event handler for laserButton"""
        weapon = self.battle.playerShip.weapons[0]
        target = self.battle.enemyShip
        self.battle.weaponControl.fireWeapon( weapon, target )
    
    def onFireMissileButtonClick( self ):
        """Event handler for missile button"""
        weapon = self.battle.playerShip.weapons[1]
        target = self.battle.enemyShip
        self.battle.weaponControl.fireWeapon( weapon, target )
                       

'''
class Bar
    A class representing a display bar or gauge on the canvas
    attributes:
        UserInterface       interface
        string              orientation {property}
        Point               corner {represents the upper-left corner of a horizontal bar
                                    or the lower-left corner of a vertical one}
        int                 width
        int                 length
        int                 scaleMin
        int                 scaleMax
        string              color
        rectangle&          display
        rectangle&          border
    instance methods:
        constructor         Bar( UserInterface interface, string orientation='horizontal',
                                 Point corner=Point(0 ,0), width=40, length=100,
                                 int scaleMin=0, int scaleMax=10 )
        void                update( newVal )
'''
class Bar( object ):
    """Represents a display bar or gauge on the canvas
    attributes:
        interface (UserInterface)
        orientation (str, property)
        corner (Point): represents the upper-left corner of a horizontal bar
                            or the lower-left corner of a vertical one
        width (int)
        length (int)
        scaleMin (int)
        scaleMax (int)
        color (str): A hex string representing the color of the bar
        display (rectangle&)
        border (rectangle&)
        
    instance methods:
        Bar( interface, orientation='horizontal',
             corner=Point(0 ,0), width=40, length=100,
             scaleMin=0, scaleMax=10 )
        update( newVal )
    """
    def __init__( self, interface, orientation='horizontal',
                  corner=Point(0, 0), width=40, length=100,
                  scaleMin=0, scaleMax=10, color='#0000FF' ):
        # Set internal attributes
        self.interface = interface
        self.orientation = orientation
        self.corner = corner
        self.width = width
        self.length = length
        self.scaleMin = scaleMin
        self.scaleMax = scaleMax
        self.color = '#0000FF'
        
        # Place bar on canvas
        if self.orientation == 'horizontal':
            upperLeft = self.corner.coords()
            lowerRight = ( self.corner + Point(self.length, self.width) ).coords()
        elif self.orientation == 'vertical':
            upperLeft = ( self.corner + Point( 0, -self.length ) ).coords()
            lowerRight = ( self.corner + Point( self.width, 0 ) ).coords()
        self.display = self.interface.canvas.create_rectangle( *upperLeft,
                                                               *lowerRight,
                                                               fill=self.color )
        self.border = self.interface.canvas.create_rectangle( *upperLeft,
                                                               *lowerRight,
                                                               width=3 )
    
    @property
    def orientation( self ):
        return self._orientation
    
    @orientation.setter
    def orientation( self, newVal ):
        isValid = (newVal == 'horizontal' or newVal == 'vertical')
        if not isValid:
            raise ValueError('orientation can only take the values'
                             ' \'horizontal\' or \'vertical\'.' )
        self._orientation = newVal
    
    def update( self, newVal ):
        """update the length of the bar to reflect the new value"""
        if newVal > self.scaleMax or newVal < self.scaleMin:
            raise ValueError('The bar\'s maximum or minimum value has been exceeded.')
        
        newLength = int(self.length*newVal/self.scaleMax)
        self.interface.canvas.itemconfigure( self.display, state=tk.HIDDEN )
        if self.orientation == 'horizontal':
            upperLeft = self.corner.coords()
            lowerRight = ( self.corner + Point(newLength, self.width) ).coords()
        elif self.orientation == 'vertical':
            upperLeft = ( self.corner + Point( 0, -newLength ) ).coords()
            lowerRight = ( self.corner + Point( self.width, 0 ) ).coords()
        self.display = self.interface.canvas.create_rectangle( *upperLeft,
                                                               *lowerRight,
                                                               fill=self.color )