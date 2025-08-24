# RSA Common Modulus Attack

Writeup untuk CTF challenge kriptografi RSA yang menggunakan modulus sama dengan eksponen prima kecil berbeda.

## Challenge

Kita punya:
- `c1 ≡ m^e1 (mod n)` 
- `c2 ≡ m^e2 (mod n)`
- `e1, e2` adalah prima 10-bit (512-1023)
- Modulus `n` dan plaintext `m` sama

## Metode Serangan

### 1. Brute Force Eksponen
Coba semua kombinasi prima 10-bit `(a, b)` dan cek:
```
c1^b ≡ c2^a (mod n)
```

Jika benar, maka `a = e1` dan `b = e2`.

### 2. Extended GCD
Cari `x, y` sehingga:
```
x*e1 + y*e2 = 1
```

### 3. Recovery Plaintext
```
m ≡ c1^x * c2^y (mod n)
```

## Penggunaan

```bash
python3 solver/solver.py
```

Edit nilai `c1`, `c2`, dan `n` di dalam file solver.

## Contoh Challenge

```python
c1 = 0x1234...
c2 = 0x5678...  
n = 0x9abc...

# Output:
# Found exponents: e1 = 617, e2 = 787
# Flag: CTF{common_modulus_attack_works}
```

## Mengapa Berhasil?

Karena jika `x*e1 + y*e2 = 1`, maka:
```
c1^x * c2^y ≡ (m^e1)^x * (m^e2)^y ≡ m^(x*e1 + y*e2) ≡ m^1 ≡ m (mod n)
```
