import tkinter as tk

from point import Point
import constants
import weapons

class Ship(object):
    """An abstract class representing the state of any ship in the game
		attributes:
            battle      (Battle): A reference to the Battle the ship belongs to
            hull        (int, property)
            maxHull     (int)
            shield      (int)
            maxShield   (int)
            ammunition  (int)
            location    (Point)
            weapons     (list<Weapon>)
            image       (tk.PhotoImage)
		instance methods:
			Ship( battle, maxHull=10, maxShield=1,
                  ammunition=0, location=Point(0, 0) )
			_setImage( imageFile )
    """
    def __init__(self, battle, maxHull=10, maxShield=1, ammunition=0,
                 location=Point(0, 0) ):
			
        self.battle = battle
        self.maxHull = self.hull = maxHull
        self.maxShield = self.shield = maxShield
        self.ammunition = ammunition
        self.location = location
        self.weapons = []
        self.image = None
    
    def _setImage(self, imageFile):
        self.image = tk.PhotoImage( file=imageFile )
    
    @property
    def hull( self ):
        return self._hull
    
    @hull.setter
    def hull( self, newVal ):
        if newVal < 0:
            self._hull = 0
        elif newVal > self.maxHull:
            self._hull = self.maxHull
        else:
            self._hull = newVal

class PlayerShip(Ship):
    """Represents the player's ship
    static members:
		imagePath   (str)
	instance methods:
		PlayerShip( battle )
    """
    imagePath = 'images/shuttle.gif'
    def __init__(self, battle):
        Ship.__init__( self, battle, maxHull=10, maxShield=1, 
                       location=constants.playerShipLocation )
        self._setImage( PlayerShip.imagePath )
        laser = weapons.Weapon( self )
        missile = weapons.Weapon( self, damage=2,
                                  shotVelocity=250,
                                  shotImagePath='images\missile.gif' )
        self.weapons.append(laser)
        self.weapons.append(missile)

class EnemyShip(Ship):
    """Represents the enemy ship
    static members:
		imagePath (str)
	instance methods:
        EnemyShip( battle )
    """
    imagePath = 'images/stardestroyer.gif'
    def __init__(self, battle):
        Ship.__init__( self, battle, maxHull=10, maxShield=1, 
                       location=constants.enemyShipLocation )
        self._setImage( EnemyShip.imagePath )
        
        
