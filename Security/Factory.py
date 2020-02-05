from PumaFernet import PumaFernet
from AuthFer256 import AuthFer256
class Factory:
    def __init__(self):

        self.key ="0aaTE5OgWdw9nDlhCucpTzL_97-vYRnSamxQafDAUUc=" # For testing purposes only should be changed for a secure key exchange algorithm like diffie hellman

    def crypto(self, cypher):
        if cypher == 'Fernet':
            return PumaFernet(self.key)        
    

    def auth(self,cypher_hash):
        if cypher_hash == 'Fer256' :
            return AuthFer256(self.key)

    #def hash(self, name):
