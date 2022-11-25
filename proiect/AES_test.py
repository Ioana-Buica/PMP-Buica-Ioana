from os import urandom
from Crypto.Cipher import AES

"""# For Generating cipher text
secret_key = b'0123456789abcdef'
iv =  b'0123456789abcdef' 
obj = AES.new(secret_key, AES.MODE_CBC, iv)

# Encrypt the message
message = 'hello'
padded_text = message + "0"*(16-len(message))

print('Original message is: ', message)
encrypted_text = obj.encrypt(message)
print('The encrypted text', encrypted_text)

# Decrypt the message
rev_obj = AES.new(secret_key, AES.MODE_CBC, iv)

decrypted_text = rev_obj.decrypt(encrypted_text)
print('The decrypted text', decrypted_text.decode('utf-8'))"""

key = 'pass_mass_123456'
IV='0123456789abcdef'
mode = AES.MODE_CBC
#encode the key and IV
encryptor = AES.new(key.encode('utf-8'), mode,IV=IV.encode('utf-8'))
# pad the text to 16bytes
text = 'hello'
padded_text = text + "|"*(16-len(text))
#encode the text
ciphertext = encryptor.encrypt(padded_text.encode("utf-8"))
print(type(ciphertext), ciphertext)

rev_obj = AES.new(key.encode('utf-8'), mode,IV=IV.encode('utf-8'))

decrypted_text = rev_obj.decrypt(ciphertext)
print(decrypted_text)
print('The decrypted text:', decrypted_text.decode('utf-8'))

