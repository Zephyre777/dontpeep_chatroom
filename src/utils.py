from Crypto.Random.random import randint
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

CIPHER_KEY_SIZE = 16 #AES-128

def KDF(sharedKey, count=1000):
    derivedKey = PBKDF2(str(sharedKey),b"",dkLen = CIPHER_KEY_SIZE,count = count)
    return derivedKey

class Client(object):
    def __init__(self, p):
        self.privateKey = 0
        self.publicKey = 0
        self.shareKey = 0
        self.p = p
        self.g = 2
        self.input = 34

    # In the initiation, to generate initial private and public key
    def pKeyGenerator(self):
        self.privateKey = (randint(1, int(self.p - 1))) #p is a 2048 bits random prime
        self.publicKey = pow(self.g, self.privateKey, self.p) #g^pkey mod p

    #When client receive a message and need to update its sharekey
    def computeSharedKeys(self, B_publicKey):
        self.shareKey = pow(self.publicKey, B_publicKey) #g^(ab) = (g^b)^a

    #Update client's public key
    def update_pkey(self):
        self.privateKey = self.privateKey + self.input
        self.publicKey = pow(self.g, self.privateKey, self.p)


class Server(object):
    def __init__(self):
        self.p = 0
        self.publicKeys={}

    def primeGenerator(self):
        self.p = (randint(1, 2048))