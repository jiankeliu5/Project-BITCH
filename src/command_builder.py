''' Functions for building APDUs to send to the RFID card '''

def polling_apdu(max_tags):
    command = [0xFF, 0x00, 0x00, 0x00, 0x04, 0xD4, 0x4A, max_tags, 0x00]    
    return command

def get_response_apdu(nbytes):
    command = [0xFF, 0xC0, 0x00, 0x00, nbytes]
    return command

def insert_reader_transmit(command):
    return get_response_apdu(len(command)) + command

def select_application_apdu(aid):   
    """ /!\ works only for aid < 255 """
    command = [0xFF, 0x00, 0x00, 0x00, 0x0C, 0xD4, 0x40, 0x01, 0x90, 0x5A, 0x00, 0x00, 0x03, aid, 0x00, 0x00, 0x00]
    return command  

def create_application_apdu(aid, key_settings, num_of_keys):
    """ /!\ works only for aid < 255 """ 
    return [0xFF, 0x00, 0x00, 0x00, 0x0E, 0xD4, 0x40, 0x01, 0x90, 0xCA, 0x00, 0x00, 0x05, aid, 0x00, 0x00, key_settings, num_of_keys, 0x00]

def delete_application_apdu(aid):
    """ /!\ works only for aid < 255 """ 
    return [0xFF, 0x00, 0x00, 0x00, 0x0C, 0xD4, 0x40, 0x01, 0x90, 0xDA, 0x00, 0x00, 0x03, aid, 0x00, 0x00, 0x00]    

def authentication_1st_step_apdu(key_no):
    return [0xFF, 0x00, 0x00, 0x00, 0x0A, 0xD4, 0x40, 0x01, 0x90, 0x0A, 0x00, 0x00, 0x01, key_no, 0x00] 

def authentication_2nd_step_apdu(deciphered_data):
    res = [0xFF, 0x00, 0x00, 0x00, 0x19, 0xD4, 0x40, 0x01, 0x90, 0xAF, 0x00, 0x00, 0x10]
    res.extend(deciphered_data)
    res.append(0x00)
    return res 

def format_PICC_apdu():
    nbytes = 8
    return [0xFF, 0x00, 0x00, 0x00, nbytes, 0xD4, 0x40, 0x01, 0x90, 0xFC, 0x00, 0x00, 0x00]               


def create_file_apdu(file_no, com_set, acc_rights, file_size):
    res = [0xFF, 0x00, 0x00, 0x00, 0x10, 0xD4, 0x40, 0x01, 0x90, 0xCD, 0x00, 0x00, 0x07]
    res.append(file_no)
    res.append(com_set)
    res.extend(acc_rights)
    res.extend(file_size)
    res.append(0x00)
    return res

def write_data_1st_step_apdu(file_no, offset, length, deciphered_data):
    data_len = 7 + len(deciphered_data)
    nbytes = 9 + data_len        
    res = [0xFF, 0x00, 0x00, 0x00, nbytes, 0xD4, 0x40, 0x01, 0x90, 0x3D, 0x00, 0x00, data_len]
    res.append(file_no)
    res.extend(offset)
    res.extend(length)
    res.extend(deciphered_data)
    res.append(0x00)
    return res
  
         
def write_data_2nd_step_adu(deciphered_data):
    data_len = len(deciphered_data)
    nbytes = 8 + data_len    
    res = [0xFF, 0x00, 0x00, 0x00, nbytes, 0xD4, 0x40, 0x01, 0x90, 0xAF, 0x00, 0x00, data_len]
    res.extend(deciphered_data)
    res.append(0x00)
    return res

def read_data_1st_step_apdu(file_no, offset, length):
    data_len = 7
    nbytes = 8 + data_len
    res = [0xFF, 0x00, 0x00, 0x00, nbytes, 0xD4, 0x40, 0x01, 0x90, 0xBD, 0x00, 0x00, data_len]
    res.append(file_no)
    res.extend(offset)
    res.extend(length)
    res.append(0x00)
    return res

def read_data_2nd_step_apdu():
    data_len = 0
    nbytes = 9
    return [0xFF, 0x00, 0x00, 0x00, nbytes, 0xD4, 0x40, 0x01, 0x90, 0xAF, 0x00, 0x00, data_len, 0x00]    
  

