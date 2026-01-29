#hej 
import hashlib

def intToByte (x: int):
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder="big")

def byteToInt (b: bytes):
    return int.from_bytes(b, byteorder="big")

def byteToHex(b: bytes) -> str:
    return b.hex()

def hexToByte(hex: str) -> bytes:
    return bytes.fromhex(hex)

def intToHex(i:int, l: int) -> str:
    return i.to_bytes(l, byteorder="big", signed=False).hex()

def hexToInt(hex: str) -> int:
    return int.from_bytes(bytes.fromhex(hex), byteorder="big", signed=False)


def sha256_bytes(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def luhn(s: str) -> bool:
    total = 0
    double = False

    for ch in reversed(s):
        d = int(ch)
        if double:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        double = not double

    return total % 10 == 0


def find_missing_digit(card: str) -> str:
    pos = card.index("X")

    for d in "0123456789":
        candidate = card[:pos] + d + card[pos+1:]
        if luhn(candidate):
            return d

    raise ValueError("No valid digit")

def main():
    print(intToHex(8888,4))

    hex4 = intToHex(8888, 4)
    b4 = hexToByte(hex4)
    digest = sha256_bytes(b4)
    print(byteToHex(digest))

    hx = "0123456789abcdef"      
    b8 = hexToByte(hx)           
    digest = sha256_bytes(b8)   
    result = byteToInt(digest)  
    print(result)

    hx = "0123456789abcdef"
    b8 = hexToByte(hx)
    result = byteToInt(b8)
    print(result)

    print("".join(find_missing_digit(line.strip())
                  for line in open("testin.txt")
                  if line.strip()))
    
if __name__ == "__main__":
    main()
