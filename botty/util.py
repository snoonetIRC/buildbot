__author__ = 'foxlet'

from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
from fabric.api import run
from fabric.context_managers import cd
import re

# Deployer builtin
# By foxlet
deploy_check_file = "[[ -f {} ]] || printf 'False'"
deploy_wget = "wget {}"
deploy_gen_hash = "openssl sha1 {}"
deploy_tar = "tar -xvf {}"
deploy_rm = "rm {}"

def deploy_builtin(snippet):
    package = snippet['package']
    dpl_pkg = package['deploy']

    deployed = False

    with cd(dpl_pkg['deploy_target']):
        if dpl_pkg['pre_deploy']:
            for item in dpl_pkg['pre_deploy']:
                res = run(item)

        if dpl_pkg['deploy_tar']:
            if run(deploy_check_file.format(dpl_pkg['deploy_tar'])) == 'False':
                res = run(deploy_wget.format(dpl_pkg['deploy_source']+dpl_pkg['deploy_tar']))
                res = run(deploy_tar.format(dpl_pkg['deploy_tar']))
            else:
                res = run(deploy_gen_hash.format(dpl_pkg['deploy_tar']))
                if res.split('=')[1].lstrip() == dpl_pkg['deploy_hash']:
                    print('Already deployed, use force mode to redo.')
                    deployed = True
                else:
                    res = run(deploy_rm.format(dpl_pkg['deploy_tar']))
                    res = run(deploy_wget.format(dpl_pkg['deploy_source']+dpl_pkg['deploy_tar']))
                    res = run(deploy_tar.format(dpl_pkg['deploy_tar']))

        if not deployed:
            if dpl_pkg['post_deploy']:
                for item in dpl_pkg['post_deploy']:
                    res = run(item)
        else:
            pass

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

# Convert string to boolean
# By foxlet
def getcheck(value):
  return str(value).lower() in ("yes", "y", "ye", "true")

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