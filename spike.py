''' S.P.I.K E. Stream Cipher'''
''' by KryptoMagick (Karl Zander) '''
from os import urandom

class SPIKE:
    def __init__(self):
        self.deck = list(range(256))
        self.j = 0
        
    def gen_rand_key(self, keylen=32):
        return urandom(keylen)
        
    def gen_rand_nonce(self, nonce_len=16):
        return urandom(nonce_len)
            
    def ksa(self, key, nonce):
        self.j = 0
        c = 0
        for i in range(256):
            self.j = (self.j + self.deck[self.j] + c) % 256
            k = key[i % len(key)]
            self.deck[self.j], self.deck[k] = self.deck[k], self.deck[self.j]
            c = (c + 1) % 256
            
        for i in range(256):
            self.j = (self.j + self.deck[self.j] + c) % 256
            k = nonce[i % len(nonce)]
            self.deck[self.j], self.deck[k] = self.deck[k], self.deck[self.j]
            c = (c + 1) % 256
    
    def update(self):
        self.j = (self.j + self.deck[self.deck[self.deck[0]]]) & 0xff
        self.deck[self.j], self.deck[0] = self.deck[self.c], self.deck[self.j]
        return self.deck[self.deck[self.deck[self.j]]]
         
    def encrypt_byte(self, b):
        num = ord(b)
        key = self.update()
        num = (num ^ key)
        return chr(num)
        
    def decrypt_byte(self, b):
        num = ord(b)
        key = self.update()
        num = (num ^ key)
        return chr(num)

    def encrypt(self, msg, key, nonce):
        self.ksa(key, nonce)
        ctxt = []
        for x in range(len(msg)):
            b = self.encrypt_byte(msg[x])
            ctxt.append(b)
        return "".join(ctxt)

    def decrypt(self, ctxt, key, nonce):
        self.ksa(key, nonce)
        ptxt = []
        for x in range(len(ctxt)):
            b = self.decrypt_byte(ctxt[x])
            ptxt.append(b)
        return "".join(ptxt)
