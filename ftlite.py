## FTLite ##
## Daniel King ##

import tkinter as tk

import ships
import controls
import ui

def main():
    """The main function that runs the game"""
    ftlite = Battle()
    ftlite.play()


class Battle(object):
    """The main class that manages the rest of the game.
    attributes:
        root           (tk.Tk): root window
        _tasks         (list<Task>): Each Task in this list consists of an action that needs
                             to happen in the next frame of animation
        _finishedTasks (list<Task>): Each Task in this list is finished and
                                     marked for deletion
        _tasksToAdd    (list<Task>): Each Task in this list will be added to the _tasks
                                  list at the beginning of the next frame of animation
        playerShip     (ships.PlayerShip)
        enemyShip      (ships.EnemyShip)
        shipControl    (controls.ShipControl)
        weaponControl  (controls.WeaponControl)
        interface      (ui.UserInterface)
        gameOver       (bool)
    instance methods:
        Battle()
        _processTasks()
        _animate() {recursively called at ~60fps}
        addTask( task )
        play()
    """
    def __init__( self ):
        self.root = tk.Tk()
        self._tasks = []
        self._finishedTasks = []
        self._tasksToAdd = []
        self.gameOver = False
        
        self.playerShip = ships.PlayerShip( self )
        self.enemyShip = ships.EnemyShip( self )
        self.shipControl = controls.ShipControl( self )
        self.weaponControl = controls.WeaponControl( self )
        self.interface = ui.UserInterface( self )
        
    @property
    def gameOver( self ):
        return self._gameOver
    
    @gameOver.setter
    def gameOver( self, state ):
        if type(state) is not bool:
            raise TypeError('gameOver must be a boolean value')
        self._gameOver = state
    
    def _processTasks( self ):
        # Move new tasks into _tasks list
        for task in self._tasksToAdd:
            self._tasks.append(task)
        
        for task in self._tasks:
            # Remove new tasks from _tasksToAdd
            if task in self._tasksToAdd:
                self._tasksToAdd.remove(task)

            # Count down upcoming tasks
            if task.state == 'upcoming':
                task.framesUntil -= 1
                if task.framesUntil == 0:
                    task.state = 'active'

            # Do active tasks
            elif task.state == 'active':
                if task.description is not None:
                    print( task.description )
                task.function()
                task.framesLeft -= 1
                if task.framesLeft == 0:
                    task.state = 'finished'
                    self._finishedTasks.append( task )
        
        #Delete finished tasks
        for task in self._finishedTasks:
            if task.state != 'finished':
                raise ValueError('Task ' + task.description + ' was designated as finished before it \
                                    was actually finished.')
            self._tasks.remove(task)
        self._finishedTasks = []

    def _animate( self ):
        self._processTasks()
        self.interface.update()
        if self.playerShip.hull == 0 or self.enemyShip.hull == 0:
            self.gameOver = True
            self.interface.onGameOver()
        if not self.gameOver:
            self.root.after(17, self._animate)
    
    def addTask( self, task ):
        self._tasksToAdd.append( task )
 
    def play( self ):
        self._animate()
        self.root.mainloop()
    
if __name__=='__main__':
    main()
    pass
