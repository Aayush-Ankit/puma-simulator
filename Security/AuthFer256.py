from IAuth import IAuth
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import sys,os

class AuthFer256(IAuth):

    def __init__(self,key):
         # Put this somewhere safe!
        self.key = key


    def generateMACModel(self,path): 
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
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
                with open(os.path.join(path1,file), 'rb') as myfile:
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
        #print(key) 
        f = Fernet(self.key)
        token = f.encrypt(hashed)
        
        #print(f.decrypt(token))
        f = open(os.path.join(path,'modelsignature.txt'), 'w')
        f.write(token)
        f.close()
        
    
    def generateMACInput(self,path): 
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        with open( os.path.join(path,'input.npy'), 'rb') as myfile:
          data = myfile.read()
        digest.update(data)
        
        
        hashed=digest.finalize()
        
        f = Fernet(self.key)
        token = f.encrypt(hashed)
        #print(token)
        f = open(os.path.join(path,'signature.txt'), 'w')
        f.write(token)
        f.close()


    
    def authenticateModel(self,path): 
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        print(path)
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
                with open(os.path.join(path1,file), 'rb') as myfile:
                  data = myfile.read()
                  digest.update(data)
            os.chdir(path)
        #print(data)
      
        hashed=digest.finalize()
        #print(hashed)
        #diff helman pra trocar chave
        #ou publica, privada
        #print(type(hashed))
       
     
         
        f = Fernet(self.key)
        token = f.encrypt(hashed)
        fs=open(os.path.join(path,"modelsignature.txt"),'r')
        sign=fs.read()
      
      
        decriptedmessage=f.decrypt(sign)
        if(decriptedmessage==hashed):
          return(True)
        return(False)
      
    def authenticateInput(self,path): 
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        with open(os.path.join(path,'input.npy'), 'rb') as myfile:
            data = myfile.read()
        digest.update(data)
    
    
        hashed=digest.finalize()
    
        #print(type(hashed))
      
       
        #print(key)
        f = Fernet(self.key)
        fs=open(os.path.join(path,'signature.txt'),'r')
        sign=fs.read()
    
    
        decriptedmessage=f.decrypt(sign)
        if(decriptedmessage==hashed):
            #print("Autenticado")
            return(True)
        return(False)


