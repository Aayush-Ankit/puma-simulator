#****************************************************************************************
# Designed by - Guilherme Maurer                
#               Miguel Xavier
#               Plinio Silveira
#               Yago Liborio
#               Pontifical Catholic University of Rio Grande do Sul 
#               
# Factory - Used to select the desired security implementation
#
#****************************************************************************************

from PumaFernet import PumaFernet
from AuthFer256 import AuthFer256
class Factory:
    def __init__(self):

        self.key ="0aaTE5OgWdw9nDlhCucpTzL_97-vYRnSamxQafDAUUc=" # For testing purposes only should be changed for a secure key exchange algorithm like diffie hellman

    #Used to select which cypher will be used for cryptography
    def crypto(self, cypher):
        if cypher == 'Fernet':
            return PumaFernet(self.key)        
        else:
            print("Invalid cryptography argument, please select a valid security implementation")
            sys.exit(1)

    #Used to select which hash and cypher will be used for authentication
    def auth(self,cypher_hash):
        if cypher_hash == 'Fer256' :
            return AuthFer256(self.key)
        else:
            print("Invalid authentication argument, please select a valid authentication implementation")
            sys.exit(1)

