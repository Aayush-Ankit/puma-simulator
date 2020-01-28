from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
def check(doc,signature):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    with open(doc, 'rb') as myfile:
        data = myfile.read()
    digest.update(data)


    hashed=digest.finalize()

    #print(type(hashed))
    # Put this somewhere safe!
    key ="0aaTE5OgWdw9nDlhCucpTzL_97-vYRnSamxQafDAUUc="
    #print(key)
    f = Fernet(key)
    fs=open(signature,'r')
    sign=fs.read()


    decriptedmessage=f.decrypt(sign)
    if(decriptedmessage==hashed):
        #print("Autenticado")
        return(True)
    return(False)