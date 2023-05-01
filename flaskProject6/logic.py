from random import shuffle

from Crypto.Util.number import getPrime, inverse
from Crypto.Random.random import randint
from math import gcd

class Authority():
    class User():
        def __init__(self, par, I, cheat=False):
            self.I = I
            self.cheat = cheat
            self.vjs = []
            self.sjs = []
            j = 0
            while (j < par.k):
                vj = par.f(I, j)
                # if(self.squareRootExists(vj, self.n)):
                if (vj in par.qrs and gcd(vj, par.n) == 1):
                    inv = inverse(vj, par.n)
                    # if(self.squareRootExists(inv, self.n)):
                    if (inv in par.qrs):
                        # sqrt = prime_mod_sqrt(inv, self.n)
                        self.vjs.append(vj)
                        # sjs.append(min(sqrt))
                        self.sjs.append(par.qrs[inv])
                        j += 1

        def getx(self, par):
            self.r = randint(0, par.n)
            return self.r ** 2 % par.n

        def gety(self, par, e):
            if (self.cheat):
                return self.r, self.vjs
            prod = self.r
            for j in range(par.k):
                if (e & 1 == 1):
                    prod *= self.sjs[j]
                e >>= 1
            return prod % par.n, self.vjs

    def __init__(self, bitlength, k, t):
        self.users = 0
        self.n = getPrime(bitlength // 2) * getPrime(bitlength // 2 + 1)
        self.k = k
        self.t = t
        self.qrs = dict()
        for i in range(self.n):
            k = (i * i) % self.n
            if (k in self.qrs):
                self.qrs[k] = min(self.qrs[k], i)
            else:
                self.qrs[k] = i

    def __getn(self):
        return self.n

    def create_user(self, I, cheat=False):
        self.users += 1
        return self.User(self, I, cheat)

    def f(self, I, j):
        return randint(0, self.n)

    def verify(self, user):
        verification = True
        for i in range(self.t):
            e = randint(0, (1 << self.k) - 1)
            x = user.getx(self)
            y, ind = user.gety(self, e)
            prod = 1
            for i, j in enumerate(ind):
                if (e & 1 == 1):
                    prod *= j
                e >>= 1
            verification &= ((y * y * prod) % self.n == x)
        return verification