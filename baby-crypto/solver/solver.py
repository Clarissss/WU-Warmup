from math import gcd
from itertools import product

def primes_in_range(lo, hi):
    hi += 1
    sieve = [True]*hi
    sieve[0:2] = [False, False]
    for p in range(2,int(hi**0.5)+1):
        if sieve[p]:
            step = p
            start = p*p
            sieve[start:hi:step] = [False]*(((hi-1-start)//step)+1)
    return [p for p in range(lo, hi) if sieve[p]]

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a, n):
    g, x, _ = egcd(a, n)
    if g != 1:
        raise ValueError("No inverse")
    return x % n

def recover_message(n, c1, c2):
    P = primes_in_range(512, 1023)
    found = None
    pow_c1 = {e: pow(c1, e, n) for e in P}  # cache helps a little
    pow_c2 = {e: pow(c2, e, n) for e in P}

    for e1, e2 in product(P, P):
        if pow_c1[e2] == pow_c2[e1]:
            found = (e1, e2)
            break
    if not found:
        raise RuntimeError("out.txt nya mana wok")

    e1, e2 = found
    g, a, b = egcd(e1, e2)
    assert g == 1

    part1 = pow(c1, a, n) if a >= 0 else modinv(pow(c1, -a, n), n)
    part2 = pow(c2, b, n) if b >= 0 else modinv(pow(c2, -b, n), n)
    m = (part1 * part2) % n
    return m, e1, e2

def n2s(x):
    blen = (x.bit_length() + 7)//8
    return x.to_bytes(blen, 'big')

if __name__ == "__main__":
    with open("out.txt","r") as f:
        n = int(f.readline().strip())
        c1 = int(f.readline().strip())
        c2 = int(f.readline().strip())

    m, e1, e2 = recover_message(n, c1, c2)
    print(f"[+] Found e1={e1}, e2={e2}")
    try:
        msg = n2s(m)
        print("[+] Flag:", msg.decode(errors="ignore"))
    except Exception:
        print("[+] Raw bytes:", n2s(m))
