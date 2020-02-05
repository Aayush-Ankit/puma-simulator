from abc import ABCMeta, abstractmethod

class IAuth:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generateMACModel(self,path): raise NotImplementedError

    @abstractmethod
    def generateMACInput(self,path): raise NotImplementedError

    @abstractmethod
    def authenticateModel(self,path): raise NotImplementedError

    @abstractmethod
    def authenticateInput(self,path): raise NotImplementedError