# Designed by - Guilherme Maurer                
#               Miguel Xavier
#               Plinio Silveira
#               Yago Liborio
#               Pontifical Catholic University of Rio Grande do Sul 
#               
# IAuth - Defines the interface used to authenticate models and input
#
#****************************************************************************************
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