from abc import ABC, abstractmethod 

class Market_Base(ABC):
    @abstractmethod
    def initializeMarketData(self):
        pass
    
    @abstractmethod
    def getPrice(self, itemname):
        pass
    
    @abstractmethod
    def getSalePrice(self, itemname):
        pass
    
    @abstractmethod
    def getUnlockTime(self, itemname):
        pass
    
    @abstractmethod
    def writeToFile(self):
        pass
    
    @abstractmethod
    def readFromFile(self):
        pass
