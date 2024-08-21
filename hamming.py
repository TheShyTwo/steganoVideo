
import numpy as np

H = np.array([
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1]
], dtype=int)

G = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1]
], dtype=int)

def encode_hamming_74(data):
    data = np.array(data)
    encoded_data = np.dot(G,data) % 2
    return encoded_data.tolist()

def decode_hamming_74(en_data):
    en_data=np.array(en_data)
    syndrome=np.dot(H,en_data) %2
    print(syndrome);
    if syndrome.sum()==0:
        return list(en_data[:4])
    else:
        pos_error=np.where(np.all(H.T==syndrome,axis=1))
        if en_data[pos_error]==0:
            en_data[pos_error]=1
        else:
            en_data[pos_error]=0
        return list(en_data[:4])
    

def encode_74(data):
    encoded_data = ''
    length = len(data)
    for index in range(0,length,4):
        list_4_bit = [int(bit) for bit in data[index:index+4]]
        list_7_bit = encode_hamming_74(list_4_bit)
        str_7_bit = ''.join([str(bit) for bit in list_7_bit])
        encoded_data += str_7_bit
    return encoded_data

def decode_74(encoded_data):
    decoded_data = ''
    length = len(encoded_data)
    for index in range(0,length,7):
        list_7_bit = [int(bit) for bit in encoded_data[index:index+7]]
        list_4_bit = decode_hamming_74(list_7_bit)
        str_4_bit = ''.join([str(bit) for bit in list_4_bit])
        decoded_data += str_4_bit
    return decoded_data



