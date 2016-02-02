import tkinter as tk
import copy

class Weapon(object):
    '''A class representing a weapon attached to a ship
       A weapon must be attached to a ship
       attributes:
           Ship             ship
           int              damage
           int              shotVelocity
           Point            location
           string           shotImagePath
           tk.PhotoImage    shotImage
           string           description
       instance methods:
           constructor      Weapon( Ship ship, int damage=1, int shotVelocity=400 )
           
    '''
    def __init__( self, ship, 
                  damage=1, 
                  shotVelocity=400, 
                  shotImagePath='images\laserBeamSmall.gif',
                  description=None):
        if type(damage) is not int or damage < 0:
            raise TypeError('Weapon damage must be a non-negative integer')
        if type(shotVelocity) is not int or shotVelocity <= 0:
            raise TypeError('Weapon shotVelocity must be a positive integer')
        
        self.ship = ship
        self.damage = damage
        self.shotVelocity = shotVelocity
        self.location = ship.location
        self.shotImagePath = shotImagePath
        self.shotImage = tk.PhotoImage( file=self.shotImagePath )
        self.description = description
        
