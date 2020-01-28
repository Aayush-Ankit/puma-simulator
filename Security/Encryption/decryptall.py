from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import sys,os

key ="0aaTE5OgWdw9nDlhCucpTzL_97-vYRnSamxQafDAUUc="
#print(key) 
f = Fernet(key)
done=0
path=sys.argv[1]
os.chdir(path) 
os.makedirs(str(path+"/decrypted"))
#os.chdir(path+'/crypto')
for root,dirs,files in os.walk(path):
  for name in dirs:
    if(name=='decrypted'): continue
    if(os.path.exists('decrypted/'+str(name))):
        done=1
        break
    os.makedirs('decrypted/'+str(name))
    path1=os.path.join(path, name)
    #print(path1)
    for root1,dirs1,files1 in os.walk(path1):
      #print(files1)
      for file in files1:
        #print(root1)
#       print(file)
        with open(path1+"/"+file, 'rb') as myfile:
          
            secretdata = myfile.read()
            data=f.decrypt(secretdata)
            with open(str(path+"/decrypted/"+name+"/"+file),'w') as decryptedfile:
                decryptedfile.write(data)
  if(done==1):
    break
          

    os.chdir(path)
#print(data)


#diff helman pra trocar chave
#ou publica, privada
#print(type(hashed))
# Put this somewhere safe!



