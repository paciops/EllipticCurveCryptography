"""Test file"""
import math
import sys
import random
import matplotlib.pyplot as plt
import base64
from Point import Point
from KoblitzAlgorithm import KoblitzAlgorithm
from ECC import ECC

class Test(object):

    def main():
        print("Welcome in test class")
        
        """I'm reading an image and trasfom it into a string"""
        """
        with open("./Elliptic_curve1.png", "rb") as image:
            b64string = base64.b64encode(image.read())
        """

        """Decode the string into ascii and trasform this string in a ascii character array"""
        #message=b64string.decode('ascii')
        message='ciao'
        msg=[]
        for c in message:
            msg.append(ord(c))

        
        """Curve on p-192r1"""
        p=int(2**192-2**64-1)
        a=int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC', 16)
        b=int('64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1', 16)
        B=Point(int('188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012',16), int('07192B95FFC8DA78631011ED6B24CDD573F977A11E794811',16))
        n=int('FFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831',16)
        #h=int('01',16)
        h=3
        seed=int('3045AE6FC8422F64ED579528D38120EAE12196D5',16)

        """Curve on p-256r1"""
        """
        p=int('FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF', 16)
        a=int('FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC', 16)
        b=int('5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B', 16)
        B=Point(int('6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296',16), int('4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5',16))
        n=int('FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551',16)
        h=int('01',16)
        seed=int('C49D360886E704936A6678E1139D26B7819F7E90',16)"""
        """Curve setting and keys generation"""
        encryptor=ECC(a,b,p, B,n,h,seed)

        (kprvM,kpubM)=encryptor.keys_generator()
        (kprvD,kpubD)=encryptor.keys_generator()

        transformer=KoblitzAlgorithm(a,b,p)
        p_message=[]
        for i in msg:
            Pm=transformer.trasform_message(i,h)
            plt.plot(Pm.X,Pm.Y, marker='o')
            if Pm!=(-1,-1) :
                p_message.append(Pm)
            print(Pm.getCoordinate())

        """Plot settings and show"""
        #plt.show()

        if p_message.__len__()!=msg.__len__():
            print("It's impossible to generate a point for this value of h")
        else:
            #Message encryption simulation
            print("Now encrypt the message")
            encrypt_message=[]
            print(p_message.__len__())
            for p in p_message:
                #for every point i'll use a different r to have different pair on same points 
                r=random.randint(1,n-1)
                encrypt_message.append(encryptor.encrypt(r, kpubD, p))
                print("Point generated")
            
            #Message decryption simulation
            print("Now you have to decrypt message")
            decrypt_message=[]
            for p in encrypt_message:
                c=encryptor.decrypt(p,kprvD)
                decrypt_message.append(c)
                print("I have decrypted a point ", c.getCoordinate())
            
            msgrcv=[]
            for p in decrypt_message:
                msgrcv.append(math.floor(p.X//h))

            s=[]
            for i in msgrcv:
                s.append(chr(i))
            
            print("Message received is ", s)

    if __name__=="__main__":
        main()
