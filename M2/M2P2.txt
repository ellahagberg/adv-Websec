import sys, hashlib

H = hashlib.sha1
HLEN = 20
K = 128

def i2osp(x, l):
    return x.to_bytes(l, "big")

def mgf1(seed, mask_len):
    t = b""
    for c in range((mask_len + HLEN - 1) // HLEN):
        t += H(seed + i2osp(c, 4)).digest()
    return t[:mask_len]

def xorb(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def oaep_encode(m_hex, seed_hex):
    m = bytes.fromhex(m_hex)
    seed = bytes.fromhex(seed_hex)
    lhash = H(b"").digest()
    ps_len = K - len(m) - 2 * HLEN - 2
    db = lhash + b"\x00" * ps_len + b"\x01" + m
    masked_db = xorb(db, mgf1(seed, K - HLEN - 1))
    masked_seed = xorb(seed, mgf1(masked_db, HLEN))
    return (b"\x00" + masked_seed + masked_db).hex()

def oaep_decode(em_hex):
    em = bytes.fromhex(em_hex.replace(" ", "").replace("\n", ""))
    masked_seed = em[1:1 + HLEN]
    masked_db = em[1 + HLEN:]
    seed = xorb(masked_seed, mgf1(masked_db, HLEN))
    db = xorb(masked_db, mgf1(seed, K - HLEN - 1))
    rest = db[HLEN:]
    i = rest.find(b"\x01")
    return rest[i + 1:].hex()

data = sys.stdin.read().split()
mode = data[0]

if mode == "mgf1":
    print(mgf1(bytes.fromhex(data[1]), int(data[2])).hex())
elif mode == "enc":
    print(oaep_encode(data[1], data[2]))
elif mode == "dec":
    print(oaep_decode("".join(data[1:])))


#för att köra a1: printf "mgf1 ea099bc94775bbe620ffde094e8ee1aa049d4894 22\n" | python3 M2P2.py
# a2 printf "enc 30c34580753883e1f421f3a012476e14b25afed894448d65aa 1e652ec152d0bfcd65190ffc604c0933d0423381\n" | python3 M2P2.py
#a3 (ändra i em.txt) printf "dec " | cat - em.txt | python3 M2P2.py
