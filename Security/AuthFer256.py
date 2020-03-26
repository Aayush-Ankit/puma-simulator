#****************************************************************************************
# Designed by - Guilherme Maurer                
#               Miguel Xavier
#               Plinio Silveira
#               Yago Liborio
#               Pontifical Catholic University of Rio Grande do Sul 
#               
# AuthFer256 - Model authentication using Fernet and SHA256
#
#****************************************************************************************







from IAuth import IAuth
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import sys,os
import time

class AuthFer256(IAuth):

    def __init__(self,key):
         # Put this somewhere safe!
        self.key = key


    # Goes through directories updating the SHA256 hash and generates the file with the MAC in it
    def generateMACModel(self,path):
        print("Generating Model MAC...")
        init_time = time.time()
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        os.chdir(path)
        for root,dirs,files in os.walk(path):
          for name in dirs:
            path1=os.path.join(path, name)
            for root1,dirs1,files1 in os.walk(path1):
              for file in files1:

                with open(os.path.join(path1,file), 'rb') as myfile:
                  data = myfile.read()
                  digest.update(data)
            os.chdir(path)
        
        
        
        
        hashed=digest.finalize() 
        f = Fernet(self.key)
        token = f.encrypt(hashed)
        
        
        f = open(os.path.join(path,'modelsignature.txt'), 'w')
        f.write(token)
        f.close()
        final_time = time.time() - init_time 
        print("Finished MAC generation in " + "{0:.4f}".format(final_time) + " seconds") 
        
    #Generate the MAC for the input file using SHA256 
    def generateMACInput(self,path): 
        print("Generating Input MAC...")
        init_time = time.time()
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        with open( os.path.join(path,'input.npy'), 'rb') as myfile:
          data = myfile.read()
        digest.update(data)
        
        
        hashed=digest.finalize()
        
        f = Fernet(self.key)
        token = f.encrypt(hashed)
        f = open(os.path.join(path,'signature.txt'), 'w')
        f.write(token)
        f.close()
        final_time = time.time() - init_time 
        print("Finished MAC generation in " + "{0:.4f}".format(final_time) + " seconds") 

    #Goes through the directories generating a Hash that is then compared to the MAC which is decrypted from the file  
    def authenticateModel(self,path):
        print("Authenticating Model MAC...")
        init_time = time.time() 
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        os.chdir(path)
        for root,dirs,files in os.walk(path):
          for name in dirs:
            path1=os.path.join(path, name)
            for root1,dirs1,files1 in os.walk(path1):
              for file in files1:
                with open(os.path.join(path1,file), 'rb') as myfile:
                  data = myfile.read()
                  digest.update(data)
            os.chdir(path)
      
        hashed=digest.finalize()
         
        f = Fernet(self.key)
        token = f.encrypt(hashed)
        fs=open(os.path.join(path,"modelsignature.txt"),'r')
        sign=fs.read()
      
      
        decriptedmessage=f.decrypt(sign)
        final_time = time.time() - init_time 
        print("Finished Model Authentication in " + "{0:.4f}".format(final_time) + " seconds") 
        if(decriptedmessage==hashed):
          return(True)
        return(False)
        
    #Generates a Hash from the input file that is then compared to the MAC which is decrypted from the file
    def authenticateInput(self,path):
        print("Authenticating Input MAC...")
        init_time = time.time() 
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        with open(os.path.join(path,'input.npy'), 'rb') as myfile:
            data = myfile.read()
        digest.update(data)
        hashed=digest.finalize()
    
        f = Fernet(self.key)
        fs=open(os.path.join(path,'signature.txt'),'r')
        sign=fs.read()
    
    
        decriptedmessage=f.decrypt(sign)
        final_time = time.time() - init_time 
        print("Finished Input Authentication in " + "{0:.4f}".format(final_time) + " seconds") 
        if(decriptedmessage==hashed):
            return(True)
        return(False)


