import cv2
from hamming import *
from aeslib import *

def msg_to_bin(msg):
    msg+='#####'
    return ''.join([format(ord(i),'016b') for i in msg])

def bin_to_dec(str_bit):
    dec=0
    bits=[int(i) for i in str_bit]
    for i in range(len(bits)):
        dec+=bits[i]*(2**(len(bits)-i-1))
    return dec


def stegano_img(img,msg_bit,index):
    for row in img:
        for pixel in row:
            for i in range(3):
                if index>=len(msg_bit):
                    return img,index
                color=format(pixel[i],"08b")
                color=color[:-1]+msg_bit[index]
                pixel[i]=bin_to_dec(color)
                index+=1
    return img, index

def stegano_video(video_path, msg_bit, output_path):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    size=(frame_width,frame_height)
    out = cv2.VideoWriter(output_path, fourcc,frame_fps, size)
    index=0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if index >=len(msg_bit):
            out.write(frame)
            continue
        else:
            frame,index=stegano_img(frame,msg_bit,index)      
            out.write(frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('successfully')
    
def get_msg_video(video_path,length):
    msg_bits=''
    msg=''
    cap=cv2.VideoCapture(video_path)
    index=0
    while True:
        ret,frame=cap.read()
        if not ret:
            break
        for row in frame:
            for pixel in row:
                for color in pixel:
                    color_bits=format(color,"08b")
                    msg_bits+=color_bits[-1]
                    if index == length-1:
                        cap.release()
                        cv2.destroyAllWindows()
                        return msg_bits
                    index+=1
        cap.release()
        cv2.destroyAllWindows()

def embed_data_to_video(input_video_path, output_video_path,plaintext, key, padding):
    encrypted_pad_data = encrypt_padding_data(plaintext, padding, key)
    encoded_pad_data = encode_hamm_padding_data(encrypted_pad_data)
    stegano_video(input_video_path, encoded_pad_data,output_video_path)
                               
def extract_data(video_path, key, padding, length_block):
    length_padding = int(length_block * 7 / 4)
    pad_embed = get_msg_video(video_path,length_padding)
    length = decrypt_padding(padding, pad_embed, key)
    if length == 0:
        return 'not found text !!!'
    else:
        length_embed_data = length + length_padding
        data_embed_pad = get_msg_video(video_path, length_embed_data)
        data_embed = data_embed_pad[length_padding:]
        data_encrypted = decode_74(data_embed)
        data = decrypt(data_encrypted, key)
        return data
    
def extract_data_from_video(video_path, key, padding, length_block):
    length_padding = int(length_block * 7 / 4)
    pad_embed = get_msg_video(video_path,length_padding)
    length = decrypt_padding(padding, pad_embed, key)
    if length == 0:
        return 'not found text !!!'
    else:
        length_embed_data = length + length_padding
        data_embed_pad = get_msg_video(video_path, length_embed_data)
        return data_embed_pad
    
def decode_hamm(data_embed_pad):
    decoded_hamm_data_pad = decode_74(data_embed_pad)
    return decoded_hamm_data_pad

def decrypt_data(decoded_hamm_data_pad, length_block, key):
    data = decrypt(decoded_hamm_data_pad[length_block:], key)
    return data

def count_volume(video_path):
    cap=cv2.VideoCapture(video_path)
    ret, frame=cap.read()
    size=np.size(frame)
    count=1
    while True:
        ret, frame=cap.read()
        if not ret:
            break
        count+=1
    cap.release()
    cv2.destroyAllWindows()
    return count*size/128/8

def play_video_lib(video_path):
    cap=cv2.VideoCapture(video_path)
    while True:
        ref,frame=cap.read()
        if ref:
            cv2.imshow('play video',frame)
            if cv2.waitKey(25) & 0xFF == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

def read_file_as_bytes(file_path):
    with open(file_path, 'rb') as file:
        byte_data = file.read()
    return byte_data

def write_bytes_to_file(byte_data, file_path):
    with open(file_path, 'wb') as file:
        file.write(byte_data)

def read_file(file_path):
    with open(file_path,'r',encoding='utf-8') as file:
        plaintext = file.read()
    return plaintext

