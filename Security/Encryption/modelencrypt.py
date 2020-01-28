from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import sys,os
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
path=sys.argv[1]
os.chdir(path)
for root,dirs,files in os.walk(path):
  for name in dirs:
    path1=os.path.join(path, name)
    #print(path1)
    for root1,dirs1,files1 in os.walk(path1):
      #print(files1)
      for file in files1:
        #print(root1)
#       print(file)
        with open(path1+"/"+file, 'rb') as myfile:
          data = myfile.read()
          digest.update(data)
    os.chdir(path)
#print(data)

hashed=digest.finalize()
#print(hashed)
#diff helman pra trocar chave
#ou publica, privada
#print(type(hashed))
# Put this somewhere safe!
key ="0aaTE5OgWdw9nDlhCucpTzL_97-vYRnSamxQafDAUUc="
#print(key) 
f = Fernet(key)
token = f.encrypt(hashed)

#print(f.decrypt(token))
f = open(str('modelsignature.txt'), 'w')
f.write(token)
f.close()