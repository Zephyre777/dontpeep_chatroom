from Crypto.Util import number
from Crypto.Random.random import randint
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

CIPHER_KEY_SIZE = 16 #AES-128

def KDF(sharedKey, count=1000):
    derivedKey = PBKDF2(str(sharedKey),b"",dkLen = CIPHER_KEY_SIZE,count = count)
    return derivedKey

class Client(object):
    def __init__(self, p):
        self.p = p
        self.privateKey = randint(1, int(self.p - 1))
        self.publicKey = 0
        self.shareKey = 0
        self.g = 2
        self.input = 34
        self.pKeyGenerator()

    # In the initiation, to generate initial private and public key
    def pKeyGenerator(self):
        self.publicKey = pow(self.g, self.privateKey, self.p) #g^pkey mod p

    # When client receive a message and need to update its sharekey
    def computeSharedKeys(self, B_publicKey):
        self.shareKey = pow(self.publicKey, B_publicKey) #g^(ab) = (g^b)^a

    # Update client's public key
    def update_pkey(self):
        self.privateKey = self.privateKey + self.input
        self.publicKey = pow(self.g, self.privateKey, self.p)

class Client_instance(object):
    def __init__(self):
        self.name
        self.socket


class Server(object):
    def __init__(self,prime_size=2048):
        self.p = (number.getPrime(prime_size))
        self.publicKeys=[]

    def updateUserPkey(self, id, pkey):
        self.publicKeys[id] = pkey

    
