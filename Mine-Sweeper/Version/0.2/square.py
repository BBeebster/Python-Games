class Square:
    def __init__(self, isMine, isFlag, isKnown, nearby):
        self.isMine = isMine
        self.isFlag = isFlag
        self.isKnown = isKnown
        self.nearby = nearby

    def show(self):
        print(f"Flag is {self.isFlag}, Mine is {self.isMine}, is Known {self.isKnown}, nearby: {self.nearby}")

    def checkMine(self):
        if self.isMine is True:
            return True
        else:
            return False

    def checkFlag(self):
        if self.isFlag is True:
            return True
        else:
            return False
    
    def checkKnown(self):
        if self.isKnown is True:
            return True
        else:
            return False
        
    def checkNearby(self):
        n = self.nearby
        return n

    def setMine(self):
        self.isMine = True
        return self

    def setFlag(self):
        if self.isFlag is False:
            self.isFlag = True
            return self
        else:
            self.isFlag = False
            return self
        
    def setKnown(self):
        if self.isKnown is False:
            self.isKnown = True
            return True
        
    def setUnknown(self):
        if self.isKnown is True:
            self.isKnown = False
            return False
    
    def upNearby(self):
        self.nearby += 1