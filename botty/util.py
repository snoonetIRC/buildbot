__author__ = 'foxlet'

from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
from fabric.api import run
import re


# Find architectures of servers via SSH
# By foxlet
def find_arch(list):
    res = run('uname -m')
    if res == 'x86_64':
        bits = 64
    elif res == 'i686':
        bits = 32
    else:
        bits = None
    list.append(bits)

# Find average uptimes of servers via SSH
# By foxlet
pattern = re.compile(r'up (\d+) days')
def uptime(times):
    res = run('uptime')
    match = pattern.search(res)
    if match:
        days = int(match.group(1))
        times['uts'].append(days)

# AES encryption/decryption utilities
# By Thijs van Dien

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)