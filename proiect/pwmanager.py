import sys
from Crypto.Cipher import AES

IV='0123456789abcdef'
mode = AES.MODE_CBC

def passDecrypt(password, master_password:str) -> str:

    if len(master_password) > 16:
        return "master_password nu este buna"

    elif len(master_password) < 16:
        master_password = master_password + "0"*(16-len(master_password))    

        decryptor = AES.new(master_password.encode('utf-8'), 
                            mode,
                            IV=IV.encode('utf-8'))

        try:
            decrypted_text = decryptor.decrypt(password)

            decrypted_text = decrypted_text.decode('utf-8').split("0")
            decrypted_text = decrypted_text[0]

            return decrypted_text

        except (UnicodeEncodeError,UnicodeDecodeError) as err:
            return False

def passEncrypt(password:str, master_password:str) -> str:

    if len(master_password) > 16:
        return "master_password nu este buna"

    else:
        master_password = master_password + "0"*(16-len(master_password))    
        encryptor = AES.new(master_password.encode('utf-8'), mode, IV=IV.encode('utf-8'))

        if len(password) > 16:
            return "password nu este buna"

        else:
            text = password + "0"*(16-len(password))
            ciphertext = encryptor.encrypt(text.encode("utf-8"))
            
            """print(master_password, text)
            print(ciphertext)
            print(ciphertext.decode("cp1252"))"""
            return ciphertext
import codecs

def operationADD(master_password,website,username,password):
    file_name = "proiect\pwmanager.db"
    database = open(file_name,"r+b") 
    password = passEncrypt(password, master_password)

    insertText = website + " " + username + " " #+ str(password) + "\n"
    database.write(bytes(insertText,"ascii"))
    database.write(password)
    database.write(bytes("\n","ascii"))

    database.close()

def operationGET(master_password,website):
    file_name = "proiect\pwmanager.db"
    database = open(file_name,"r") # Read Only (‘r’)

    info = database.readlines()

    for lineText in info:
        line = lineText.split()

        if website == line[0]:
            text = passDecrypt(line[2],master_password)
            if text != False:
                print(lineText)

    database.close()
            

def operationREMOVE(master_password,website):
    file_name = "proiect\pwmanager.db"
    database = open(file_name,"w+") # Write and Read (‘w+’) 

    info = database.readlines()
    infoCopy = info

    for i in range(0,len(info)):
        lineText = info[i]
        line = lineText.split()

        if website == line[0]:
            text = passDecrypt(line[2],master_password)
            if text != False:
                if lineText in infoCopy:
                    infoCopy.remove(lineText)

    database.truncate(0)
    database.writelines(infoCopy)

    database.close()

def operationLIST(master_password: str):
    file_name = "proiect\pwmanager.db"
    database = open(file_name,"rb") # Read Only (‘r’)

    info = database.read()
    text = passDecrypt(info,master_password)

    if text != False:
        print(text)

    """for lineText in info:
        line = lineText.split()

        text = passDecrypt(line[2],master_password)
        if text != False:
            print(lineText[:-1])"""
    
    database.close()
        
def getOperation(listArgv: list):

    master_password = listArgv[1]
    operation = listArgv[2]

    if operation == "-add":
        if len(sys.argv) != 6:
            print("Nu sunt destule argumente pt operatiunea ", operation)
        else:
            website   = listArgv[3]
            username  = listArgv[4]
            password  = listArgv[5]

            operationADD(master_password,website,username,password)
    
    elif operation == "-remove":
        if len(sys.argv) != 4:
            print("Nu sunt destule argumente pt operatiunea ", operation)
        else:
            website   = listArgv[3]

            operationREMOVE(master_password,website)

    elif operation == "-get":
        if len(sys.argv) != 4:
            print("Nu sunt destule argumente pt operatiunea ", operation)
        else:
            website   = listArgv[3]

            operationGET(master_password,website)

    elif operation == "-list":
        operationLIST(master_password)

    else:
        print("operatiune gresita:", operation)

if __name__ == "__main__":

    #pwmanager.py <master_password> -<operation> <website> <username> <password>
    if len(sys.argv) > 6:
        print("Prea multe argumente")
    else:
        getOperation(sys.argv)
