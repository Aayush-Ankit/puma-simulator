#****************************************************************************************
# Designed by - Guilherme Maurer                
#               Miguel Xavier
#               Plinio Silveira
#               Yago Liborio
#               Pontifical Catholic University of Rio Grande do Sul 
#               
# ICryptography - Defines the interface used to encrypt and decrypt models
#
#****************************************************************************************
from abc import ABCMeta, abstractmethod

class ICryptography:
    __metaclass__ = ABCMeta

    #Encrypts a model
    @abstractmethod
    def encrypt(self,path): raise NotImplementedError
    #Decrypts a model
    @abstractmethod
    def decrypt(self,path): raise NotImplementedError