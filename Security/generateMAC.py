#****************************************************************************************
# Designed by - Guilherme Maurer                
#               Miguel Xavier
#               Plinio Silveira
#               Yago Liborio
#               Pontifical Catholic University of Rio Grande do Sul 
#               
# GenerateMAC - A script that calls functions to generate MAC for Model and Input
#
#****************************************************************************************

from Factory import Factory
import sys

if __name__ == "__main__":
    cypher_hash = sys.argv[1]
    path = sys.argv[2]
    f = Factory()
    puma_cypher_hash = f.auth(cypher_hash)
    puma_cypher_hash.generateMACModel(path)
    puma_cypher_hash.generateMACInput(path)