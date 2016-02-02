## Controls and User Interfaces for FTLite ##
import tkinter as tk

import constants
from decorators import returnFunc
from task import Task

class ShipControl(object):
    """Represents the actions that can be done with a Ship
    attributes:
        battle (Battle): A reference to the Battle the ShipControl belongs to
    instance methods:
        ShipControl(Battle battle)
        addWeapon(Ship ship, Weapon weapon) {@returnFunc}
        changeHull(Ship ship, int delta) {@returnFunc}
    """
    def __init__( self, battle ):
        self.battle = battle
    
    @returnFunc
    def addWeapon( self, ship, weapon ):
        ship.weapons.append( weapon )
    
    @returnFunc
    def changeHull( self, ship, delta ):
        ship.hull += delta
    
class WeaponControl(object):
    """Represents the actions that can be done with a Weapon or Shot
    attributes:
        battle (Battle): A reference to the Battle the WeaponControl belongs to
    instance methods:
        WeaponControl(Battle battle)
        fireWeapon(Weapon weapon, Ship target)
    """
    def __init__( self, battle ):
        self.battle = battle
        
    def fireWeapon( self, weapon, target ):
        """Fires a weapon at a target.
        
        Creates a shot on the canvas and adds tasks to the main battle
        task list to move the shot, hide the shot when it impacts,
        and damage the target ship.
        """
        def printFireMessage():
            print('Firing weapon')
        distanceToTarget = int( weapon.location.distanceTo( target.location ) )
        timeToTarget = 60 * int( distanceToTarget / weapon.shotVelocity )
        shot = self.battle.interface.canvas.create_image( *weapon.location.coords(),
                                                          image=weapon.shotImage )
        dxPerFrame = (target.location.x - weapon.location.x)//timeToTarget
        dyPerFrame = (target.location.y - weapon.location.y)//timeToTarget
        fire = Task(   function=printFireMessage,
                       framesLeft=1, 
                       framesUntil=0,
                       state='active',
                       description=None )
        travel = Task( function=self.battle.interface.moveShot( shot, dxPerFrame, dyPerFrame ),
                       framesLeft=timeToTarget,
                       framesUntil=0,
                       state='active',
                       description=None )
        impact = Task( function=self.battle.shipControl.changeHull( target, -weapon.damage ),
                       framesLeft=1,
                       framesUntil=timeToTarget,
                       state='upcoming',
                       description='Shot impacting target' )
        shotEnd = Task( function=self.battle.interface.itemConfigure( shot, state=tk.HIDDEN ),
                        framesLeft=1,
                        framesUntil=timeToTarget,
                        state='upcoming',
                        description=None )
                    
        self.battle.addTask( fire )
        self.battle.addTask( travel )
        self.battle.addTask( impact )
        self.battle.addTask( shotEnd )
        


    

