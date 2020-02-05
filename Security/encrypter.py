from Factory import Factory
import sys

if __name__ == "__main__":
    encrypt = sys.argv[1]
    path = sys.argv[2]
    f = Factory()
    puma_encrypter = f.crypto(encrypt)
    puma_encrypter.encrypt(path)