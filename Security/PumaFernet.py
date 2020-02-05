from cryptography.fernet import Fernet
import sys,os,shutil
from ICryptography import ICryptography

class PumaFernet(ICryptography):

    def __init__(self,key):
        self.key = key

    def encrypt(self,path):
      #print(key) 
      f = Fernet(self.key)
      done=0
      #path=sys.argv[1]
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
              
    
    

    
    def decrypt(self,path):
      #path="/home/guilherme/Documents/PumaGithub/puma-simulator/test/testasm/lstm/crypto"
    
      #print(key) 
      f = Fernet(self.key)
      done=0
    
      os.chdir(os.path.join(path,"crypto")) # model/crypto
      crypto_path = os.path.join(path,"crypto")
      for root,dirs,files in os.walk(crypto_path):
        for name in dirs:
          if(os.path.exists(os.path.join(path,str(name)))):
              done=1
              break
          os.makedirs(os.path.join(path,str(name)))
          path1=os.path.join(crypto_path, name)
          #print(path1)
          for root1,dirs1,files1 in os.walk(path1):
            #print(files1)
            for file in files1:
              #print(root1)
      #       print(file)
              with open(os.path.join(path1,file), 'rb') as myfile:
                
                  secretdata = myfile.read()
                  data=f.decrypt(secretdata)
                  with open(str(path+"/"+name+"/"+file),'w') as decryptedfile:
                      decryptedfile.write(data)
        if(done==1):
          break
                
    
          os.chdir(path)
    #print(data)
    
    

    




