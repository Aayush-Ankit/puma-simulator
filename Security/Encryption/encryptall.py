from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import sys,os,shutil

key ="0aaTE5OgWdw9nDlhCucpTzL_97-vYRnSamxQafDAUUc="
#print(key) 
f = Fernet(key)
done=0
path=sys.argv[1]
os.chdir(path) 
if os.path.exists(path+'/crypto'):
  shutil.rmtree(path+'/crypto')
os.makedirs(str(path+"/crypto"))
#os.chdir(path+'/crypto')
for root,dirs,files in os.walk(path):
  for name in dirs:
    if(name=='crypto'): continue
    if(os.path.exists('crypto/'+str(name))):
        done=1
        break
    os.makedirs('crypto/'+str(name))
    path1=os.path.join(path, name)
    #print(path1)
    for root1,dirs1,files1 in os.walk(path1):
      #print(files1)
      for file in files1:
        #print(root1)
#       print(file)
        with open(path1+"/"+file, 'rb') as myfile:
          
            data = myfile.read()
            secretdata=f.encrypt(data)
            with open(str(path+"/crypto/"+name+"/"+file),'w') as secretfile:
                secretfile.write(secretdata)
  if(done==1):
      break
          


#print(data)



