import sys

from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.System import readers
from smartcard.util import toHexString
from threading import Timer
from Crypto import PublicKey
import Crypto.PublicKey.RSA
from loyalty_card import *
import readline # just adding this line improves raw_input() edition capabilities


connection = None

""" Encryption/Decryption keys """
P_K_enc = None 
P_K_shop = None
P_ca = None

def print_welcome():
    print "Welcome to sandwich-manager beta release."
    r=readers() 
    if len(r) < 1:
        print "Warning: no reader available"         
    else:
        print "Reader: "+str(r[0])  
    print "Type 'help' or 'h' for help."	

def print_help():  
    print "init    : initialize a new RFID loyalty card"
    print "reset  : reset an RFID loyalty card to factory settings"
    print "read    : read the content of an RFID loyalty card"
    print "buy     : add a purchase to an RFID loyalty card"
    print "quit    : try to guess" 


def init_loyalty_card(p_k_enc, p_k_shop, p_ca, conn):    
    card = LoyaltyCard(p_k_enc, p_k_shop, p_ca, conn)
    t = Timer(3.0, reminder)
    t.start()
    card.poll();  
    t.cancel()
    try:
        card.initialize()
    except TagException as instance:
        print instance.msg
    else:
        print "Loyalty card successfully initialized"    

def reset_loyalty_card(p_k_enc, p_k_shop, p_ca, conn):    
    card = LoyaltyCard(p_k_enc, p_k_shop, p_ca, conn)  
    t = Timer(3.0, reminder)
    t.start()
    card.poll(); 
    t.cancel()
    try:
        card.reset()
    except TagException as instance:
        print instance.msg
    else: 
        print "Loyalty card successfully reset to factory settings"

def read_loyalty_card(p_k_enc, p_k_shop, p_ca, conn):
    card = LoyaltyCard(p_k_enc, p_k_shop, p_ca, conn)
    t = Timer(3.0, reminder)
    t.start()
    card.poll();    
    t.cancel()        
    print card.get_counter()
    print card.get_log()

def buy_sandwich(n, p_k_enc, p_k_shop, p_ca, conn):
    card = LoyaltyCard(p_k_enc, p_k_shop, p_ca, conn)
    t = Timer(3.0, reminder)
    t.start()
    card.poll(); 
    t.cancel()            
    card.add_sandwich(n)
    print str(n)+" purchase(s) correctly added to the loyalty card"

def check_reader_availability():
    global connection
    r=readers() 
    if len(r) < 1:
        print "Warning: no reader available"    
    else:
        connection = r[0].createConnection()
        connection.connect()  
        
def reminder():
    print "No card detected! Please insert a card."  

def read_keys():
    global P_K_enc, P_K_shop, P_ca     
    try:
        key = open('./keys/P_enc--loyaltyEncryptionPublic.key').read()
        P_K_enc = PublicKey.RSA.importKey(key)    
        key = open('./keys/K_enc--loyaltyEncryptionPrivate.key').read()
        P_K_enc = PublicKey.RSA.importKey(key)  
        key = open('./keys/P_CA--CAPublicKey.key').read()  
        P_ca = PublicKey.RSA.importKey(key)
        key = open('./keys/Attrapez-les-tous_RSAprivate.key').read()  
    except IOError:
        print """
    Need the files:
    ./keys/P_enc--loyaltyEncryptionPublic.key
    ./keys/K_enc--loyaltyEncryptionPrivate.key
    ./keys/P_CA--CAPublicKey.key  
    ./keys/Attrapez-les-tous_RSAprivate.key  
    """
        exit(-1)


def main_loop():
    while 1:
        check_reader_availability()
        try:
            command = raw_input("$sandwich-manager> ") 	 
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        
        if command == "h" or command == "help":
            print_help()
        elif command == "init":
            init_loyalty_card(P_K_enc, P_K_shop, P_ca, connection)
        elif command == "reset":
            reset_loyalty_card(P_K_enc, P_K_shop, P_ca, connection)
        elif command == "read":
            read_loyalty_card(P_K_enc, P_K_shop, P_ca, connection)
        elif command == "buy":
            buy_sandwich(1, P_K_enc, P_K_shop, P_ca, connection)
        elif command == "quit":
            break	
        else:
            print "Unknown command"
    connection == None or connection.disconnect()
        

def main(argv):
    print_welcome()
    read_keys()
    main_loop()
    

if __name__ == "__main__":
    main(sys.argv[1:])
