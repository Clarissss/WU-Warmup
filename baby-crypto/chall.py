from Crypto.Util.number import getPrime
from libnum import s2n
p = getPrime(512)
q = getPrime(512)
pt = s2n(open('flag.txt', 'rb').read())
ct1 = pow(pt, getPrime(10), p * q)
ct2 = pow(pt, getPrime(10), p * q)

with open('out.txt', 'w') as f:
    f.write(f'{p*q}\n{ct1}\n{ct2}\n')