class History:
    """
    Represents the history of correct or incorrect answers given
    by the child
    """

    highestLevel = 1
    totalRight = 0
    _queue = []

    # appends an answer to the end of the queue
    def add(self, boolean):
        if( not isinstance(boolean, bool) ):
            raise TypeError("parameter must be of type bool: "+str(boolean))

        if(boolean):
            self.totalRight += 1

        if( len(self._queue) < 3 ):
            self._queue.insert(0,boolean)
        else:
            self._queue.pop()
            self._queue.insert(0,boolean)

    # checks if the previous three answers were correct
    def threeRight(self):
        return self._queue == [True,True,True]

    # checks if the previous three answers were wrong
    def threeWrong(self):
        return self._queue == [False,False,False]

    # tracks the history of the level of the player
    def newLevel(self):
        if( self.threeRight() and self.highestLevel < 7 ):
              self.highestLevel += 1
        self._queue = []

    # resets this History to it's initial state
    def reset(self):
        self.highestLevel = 1
        self.totalRight = 0
        self._queue = []


