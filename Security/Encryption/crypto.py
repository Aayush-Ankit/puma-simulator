from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import sys
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
with open(sys.argv[1], 'rb') as myfile:
  data = myfile.read()
digest.update(data)


hashed=digest.finalize()

#print(type(hashed))
# Put this somewhere safe!
key ="0aaTE5OgWdw9nDlhCucpTzL_97-vYRnSamxQafDAUUc="
#print(key)
f = Fernet(key)
token = f.encrypt(hashed)
print(token)


decriptedmessage=f.decrypt(token)
if(decriptedmessage==hashed):
    print("Autenticado")
