from abc import ABCMeta, abstractmethod

class ICryptography:
    __metaclass__ = ABCMeta

    @abstractmethod
    def encrypt(self,path): raise NotImplementedError

    @abstractmethod
    def decrypt(self,path): raise NotImplementedError