''' Representation of an RFID loyalty card 
     along with methods to interact with the physical RFID card '''

from smartcard.System import readers
from smartcard.CardType import ATRCardType, AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import *
from smartcard.util import toHexString, toBytes
from command_builder import * 
from Crypto.Cipher import DES
import Crypto.Random.random
from Crypto.Random.random import *


def perform_command(conn, apdu):
    response, sw1, sw2 = conn.transmit(apdu)    
    get_resp = get_response_apdu(sw2)
    response, sw1, sw2 = conn.transmit(get_resp)
    print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)
    return response, sw1, sw2          	


class TagException(Exception):    
    def __init__(self, msg):        
        self.msg = msg
        

class LoyaltyCard:
    
    def __init__(self, conn):     
        random_gen = StrongRandom() 
        self.__connection = conn              
        self.__kdesfire = DES.new(str(random_gen.randint(10000000,99999999)), DES.MODE_ECB)
        self.__k = DES.new(str(random_gen.randint(10000000,99999999)), DES.MODE_ECB)
        self.__km1 = DES.new(str(random_gen.randint(10000000,99999999)), DES.MODE_ECB)
        self.__km2 = DES.new(str(random_gen.randint(10000000,99999999)), DES.MODE_ECB)
        self.__kw1 = DES.new(str(random_gen.randint(10000000,99999999)), DES.MODE_ECB)            

    def __select_application(self, aid):
        pass

    def __create_application(self, aid, key_settings, num_of_keys):
        apdu = create_application_apdu(aid, key_settings, num_of_keys)
        response, sw1, sw2 = perform_command(self.__connection, apdu)
        if not(response[3] == 0x91 and response[4] == 0x00 and sw1 == 0x90 and sw2 == 0x00):            
            raise TagException('Application creation has failed!')
    
    def __delete_application(self, aid):
        apdu = delete_application_apdu(aid)
        response, sw1, sw2 = perform_command(self.__connection, apdu)
        if not(response[3] == 0x91 and response[4] == 0x00 and sw1 == 0x90 and sw2 == 0x00):            
            raise TagException('Application deletion has failed!')        

    def __create_file(self, aid, no, access_rights):
        pass

    def __change_key(self, aid, key_no, new_key):
        pass

    def __authenticate(self, aid, key_no, key):
        pass

    def __write_data(self, aid, file_no, data, key):
        pass

    def __read_data(self, aid, file_no, key):
        return None

    def __verify_signature(self):
        pass

    def poll(self):
        apdu = polling_apdu(1)
        perform_command(self.__connection, apdu)        
        # the following code doesn't work with the card since the ATR is
        # wrong!!
        #cardtype = ATRCardType(toBytes( "3B 04 41 11 77 81" ))        
        #cardrequest = CardRequest( timeout=5, cardType=cardtype )
        #try:
        #    self.__cardservice = cardrequest.waitforcard()
        #except CardRequestTimeoutException:
        #    raise
        #self.__cardservice.connection.connect()
        #print toHexString( self.__cardservice.connection.getATR() )
        	

    def initialize(self):
        self.__create_application(1, 0x0B, 2)        

    def reset(self):
        self.__delete_application(1)        

    def get_counter(self):
        sk = self.__authenticate(2,1,self.__k)
        c = self.__read_data(2, 1, sk)
        return "2 sandwiches purchased so far"

    def get_log(self):
        sk = self.__authenticate(2,1,self.__k)
        log = self.__read_data(2, 2, sk)
        return "22/10/2011 - 12:51 - Subway-like\n" + "02/11/2011 - 13:28 - Bob's shop"

    def add_sandwich(self, n):
        pass

    
