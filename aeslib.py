from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
from Crypto.Random import get_random_bytes
from hamming import *

def hex_to_bit(hex_string):
    byte_data = binascii.unhexlify(hex_string)
    bit_data = ''.join(format(byte, '08b') for byte in byte_data)
    return bit_data

def bit_to_hex(bit_string):
    byte_data = bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))
    hex_data = binascii.hexlify(byte_data).decode()
    return hex_data

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plaintext.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    hex_encrypted_data = encrypted_data.hex() 
    bit_encrypted_data = hex_to_bit(hex_encrypted_data) 
    return bit_encrypted_data

def decrypt(bit_encrypted_data, key):
    hex_encrypted_data = bit_to_hex(bit_encrypted_data)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(bytes.fromhex(hex_encrypted_data))
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode()


def encrypt_padding_data(plaintext,padding,key):
    encrypted_data = encrypt(plaintext, key)
    len_en_data = len(encrypted_data)
    len_en_data74 = int(len_en_data / 4 * 7)
    padding_74 = padding + str(len_en_data74)
    pad_encrypt = encrypt(padding_74,key)
    encrypted_pad_data = pad_encrypt + encrypted_data
    return encrypted_pad_data

def encode_hamm_padding_data(encrypted_pad_data):
    encoded_pad_data = encode_74(encrypted_pad_data)
    return encoded_pad_data

def decrypt_padding(padding,pad_encode,key):
    try:
        pad_decode = decode_74(pad_encode)
        pad_decrypt = decrypt(pad_decode,key)
        if padding in pad_decrypt:
            padding_out, length = pad_decrypt.split('-')
            if (padding_out+'-') == padding :
                length = int(length)
                return length
            else:
                return 0
        else:
            return 0
    except:
        return 0





# padding = 'long-'
# file_path = 'input_text.txt'
# key = get_random_bytes(16)
# length_key = 128

# bits = encrypt_padding(file_path, padding, key)



