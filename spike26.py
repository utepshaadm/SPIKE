''' S.P.I.K E. 26 Stream Cipher'''
''' by KryptoMagick (Karl Zander) '''

class SPIKE26:
    def __init__(self):
        self.deck = list(range(26))
        self.j = 0
        self.c = 0
            
    def ksa(self, key, nonce):
        self.j = 0
        c = 0
        for i in range(26):
            self.j = (self.j + self.deck[self.j] + c) % 26
            k = key[i % len(key)]
            self.deck[self.j], self.deck[k] = self.deck[k], self.deck[self.j]
            c = (c + 1) % 26
            
        for i in range(26):
            self.j = (self.j + self.deck[self.j] + c) % 26
            k = nonce[i % len(nonce)]
            self.deck[self.j], self.deck[k] = self.deck[k], self.deck[self.j]
            c = (c + 1) % 26
    
    def update(self):
        self.j = (self.j + self.deck[self.deck[self.c]]) % 26
        o = self.deck[self.deck[self.deck[self.j]]]
        self.deck[self.j], self.deck[self.c] = self.deck[self.c], self.deck[self.j]
        self.c = (self.c + 1) % 26
        return o
         
    def encrypt_byte(self, b):
        num = ord(b) - 65
        key = self.update()
        num = (num + key) % 26
        return chr(num + 65)
        
    def decrypt_byte(self, b):
        num = ord(b) - 65
        key = self.update()
        num = (num - key) % 26
        return chr(num + 65)

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
