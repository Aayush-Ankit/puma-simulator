#****************************************************************************************
# Designed by - Guilherme Maurer                
#               Miguel Xavier
#               Plinio Silveira
#               Yago Liborio
#               Pontifical Catholic University of Rio Grande do Sul 
#               
# PumaFernet - Model encryption and decryption
#
#****************************************************************************************


from cryptography.fernet import Fernet
import sys,os,shutil
from ICryptography import ICryptography
import time

class PumaFernet(ICryptography):

    def __init__(self,key):
        self.key = key

    #Encrypt the files contained in tiles' folders using Fernet
    def encrypt(self,path):
      print("Fernet encryption")
      init_time = time.time() 
      f = Fernet(self.key)
      done=0

      os.chdir(path) 
      if os.path.exists(path+'/crypto'):
        shutil.rmtree(path+'/crypto')
      os.makedirs(str(path+"/crypto"))
      for root,dirs,files in os.walk(path):
        for name in dirs:
          if(name=='crypto'): continue
          if(os.path.exists('crypto/'+str(name))):
              done=1
              break
          os.makedirs('crypto/'+str(name))
          path1=os.path.join(path, name)
          
  
          print("Encrypting "+name+"...")
          for root1,dirs1,files1 in os.walk(path1):
            for file in files1:
              with open(path1+"/"+file, 'rb') as myfile:
                
                  data = myfile.read()
                  secretdata=f.encrypt(data)
                  with open(str(path+"/crypto/"+name+"/"+file),'w') as secretfile:
                      secretfile.write(secretdata)
          
        if(done==1):
            break
      final_time = time.time() - init_time 
      print("Finished encryption in " + "{0:.4f}".format(final_time) + " seconds")  
    
    

    #Decrypt the files contained in tiles' folders using Fernet
    def decrypt(self,path):
      print("Decrypting Fernet")
      f = Fernet(self.key)
      done=0
      init_time = time.time()
      os.chdir(os.path.join(path,"crypto")) 
      crypto_path = os.path.join(path,"crypto")
      for root,dirs,files in os.walk(crypto_path):
        for name in dirs:
          if(os.path.exists(os.path.join(path,str(name)))):
              done=1
              break
          os.makedirs(os.path.join(path,str(name)))
          path1=os.path.join(crypto_path, name)
          print("Decrypting "+name+"...")
          for root1,dirs1,files1 in os.walk(path1):
            for file in files1:
              with open(os.path.join(path1,file), 'rb') as myfile:
                
                  secretdata = myfile.read()
                  data=f.decrypt(secretdata)
                  with open(str(path+"/"+name+"/"+file),'w') as decryptedfile:
                      decryptedfile.write(data)
        if(done==1):
          break
                
      final_time = time.time() - init_time 
      print("Finished decryption in " + "{0:.4f}".format(final_time) + " seconds")  
    
    
    

    




