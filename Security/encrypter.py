#****************************************************************************************
# Designed by - Guilherme Maurer                
#               Miguel Xavier
#               Plinio Silveira
#               Yago Liborio
#               Pontifical Catholic University of Rio Grande do Sul 
#               
# Encrypter - A script that calls an encrypt function
#
#****************************************************************************************

from Factory import Factory
import sys

if __name__ == "__main__":
    encrypt = sys.argv[1]
    path = sys.argv[2]
    f = Factory()
    puma_encrypter = f.crypto(encrypt)
    puma_encrypter.encrypt(path)