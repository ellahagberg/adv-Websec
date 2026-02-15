#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import hashlib

import M2P3 as m2p3

def sha1_int(data: bytes) -> int:
    return int.from_bytes(hashlib.sha1(data).digest(), 'big')


def int_to_bytes(n: int) -> bytes:
    if n == 0:
        return b"\x00"
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')


if __name__ == '__main__':
    p = int(
        'ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff',
        16
    )
    g = 2

    host = "igor.eit.lth.se"
    port = 6005

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    m2p3.set_client(client)


    g_x1 = m2p3.recv_int()             
    x2 = m2p3.generate_random(p)
    g_x2 = pow(g, x2, p)
    m2p3.send_int(g_x2)               

    dh_ack = m2p3.recv_text()          
    print("alice får g^x2?:", dh_ack)

    dh_key = pow(g_x1, x2, p)         

    passphrase = "eitn41 <3".encode("utf-8")
    x_secret = sha1_int(int_to_bytes(dh_key) + passphrase)

    #receive g^a2 and send g^b2
    g_a2 = m2p3.recv_int()             
    b2 = m2p3.generate_random(p)
    g_b2 = pow(g, b2, p)
    m2p3.send_int(g_b2)               
    ack = m2p3.recv_text()             
    print("alice får g^b2?:", ack)

    #eeceive g^a3, send g^b3
    g_a3 = m2p3.recv_int()            
    b3 = m2p3.generate_random(p)
    g_b3 = pow(g, b3, p)
    m2p3.send_int(g_b3)                
    ack = m2p3.recv_text()
    print("alice får g^b3?:", ack)

    g2 = pow(g_a2, b2, p)
    g3 = pow(g_a3, b3, p)


    P_a = m2p3.recv_int()              
    s = m2p3.generate_random(p)        #bob do random
    P_b = pow(g3, s, p)                
    m2p3.send_int(P_b)                 
    ack = m2p3.recv_text()
    print("alice får Pb?:", ack)

    
    Q_a = m2p3.recv_int()              
    # Qb = g^s * g2^x 
    Q_b = (pow(g, s, p) * pow(g2, x_secret, p)) % p
    m2p3.send_int(Q_b)                 
    ack = m2p3.recv_text()
    print("alice får qb:", ack)

   
    Qab_a3 = m2p3.recv_int()          

    inv_Qb = pow(Q_b, -1, p)
    Qa_over_Qb = (Q_a * inv_Qb) % p
    Qab_b3 = pow(Qa_over_Qb, b3, p)    
    m2p3.send_int(Qab_b3)             

    #verify c
    c = pow(Qab_a3, b3, p)

    inv_Pb = pow(P_b, -1, p)
    rhs = (P_a * inv_Pb) % p

    
    auth = m2p3.recv_text()
   
    #edit for correct quiz
    m = int("2324716aa917a3bcaef65077321d993b13637729", 16)
    enc = m ^ dh_key
    m2p3.send_int(enc)

    response = m2p3.recv_text()  
    print("svar:", response)

    client.close()
