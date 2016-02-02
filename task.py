## Task for FTLite ##

class Task(object):
    """Represents a task that needs to happen in the battle's _animate method
    static members:
        validStates (dict<string, int>)
    attributes:
        function    (function): A function with no arguments that represents the action
            of the task
        framesLeft  (int)
        framesUntil (int)
        _state      (int)
        state       (string, property)
        description (string)
    """
    validStates = {"upcoming":0, "active":1, "finished":2}
    
    def __init__(self, function=None, framesLeft=1, framesUntil=0, state="active",
                    description=None):
        if type(framesLeft) is not int or type(framesUntil) is not int:
            raise TypeError('A number of frames must be an integer')
        elif framesLeft < 1 or framesUntil < 0:
            raise ValueError('The number of frames left must be positive, and \
                                the number of frames until must be non-negative.')
        elif function is None:
            raise TypeError('A Task object must be given a function')
        
        if framesUntil != 0 and state != 'upcoming':
            raise ValueError( 'A Task was labeled \'active\' or \'finished\''
                              'and was given a non-zero value for framesUntil' )
	
        self.function = function
        self.framesLeft = framesLeft
        self.framesUntil = framesUntil
        self.description = description
        if self.framesUntil:
            self.state = 'upcoming'
        else:
            self.state = 'active'
    
    @property
    def state(self):
        for name, num in Task.validStates.items():
            if self._state==num:
                return name
            else:
                continue
    
    @state.setter
    def state( self, name ):
        if name not in Task.validStates.keys():
            raise ValueError('That is not a valid name for a Task state.')
        
        self._state = Task.validStates[name]
