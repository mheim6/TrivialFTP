#Monica Heim
#Homework 1
#Computer Networks
from socket import *
import argparse
import sys

# Args
parser = argparse.ArgumentParser(description='Flags for the transfer')
parser.add_argument('-a',
                    "--ip",
                    type=str,
                    action='store',
                    help='IP address to connect to',
                    required=True)
parser.add_argument('-p',
                    "--port",
                    type=int,
                    action="store",
                    help='port to use',
                    required=True)
parser.add_argument('-sp',
                    "--serverPort",
                    type=int,
                    action="store",
                    help='server port to use',
                    required=True)
parser.add_argument('-f',
                    "--file",
                    type=str,
                    action='store',
                    help='filename to read or write',
                    required=True)
parser.add_argument('-m',
                    "--mode",
                    type=str,
                    action='store',
                    help='mode for file',
                    required=True)
args = parser.parse_args()


def main():
    pport = args.port
    server = args.ip
    servport = args.serverPort


    # Check to see if IP is correct
    ls = server.split('.')
    if len(ls) is not 4:
        print('IP not correct')
        sys.exit()
    for a in ls:
        if not a.isdigit():
            print('IP not correct')
            sys.exit()
        i = int(a)
        if i < 0 or i > 255:
            print('IP not correct')
            sys.exit()
    print('IP is correct')
    if pport < 5000 or pport > 65535:
        sys.exit(1)
    # checks port
    if servport < 5000 or servport > 65535:
        print('Port not correct')
        sys.exit()
    print('Port is correct')
    mode = args.mode
    filename = args.file
    serverAdd = (server, servport)
    try:
        clientSocket = socket(AF_INET, SOCK_DGRAM)
    except clientSocket.error as msg:
        print("error message.")
        sys.exit(1)

    if mode == "r":
        fillet = open(filename, "wb")
        pack = read(filename)
        clientSocket.sendto(pack, serverAdd)
        message = clientSocket.recv(516)
        mstring = str(message, 'ascii', 'replace')
        mstring = mstring[4:]
        met = message[4:]
        fillet.write(met)
        if filename == 'bigfile':
            mstring = mstring[:1] + "" + mstring[1 + 1:]
        file_str = mstring
        isData = True
        if message[1] == 3:
            isData = True
        else:
            isData = False
        while isData:
            if message[2] == 255 and message[3] == 255:
                isData = False
                break
            clientSocket.sendto(ack(message[2], message[3]), serverAdd)
            message, addr = clientSocket.recvfrom(516)
            mstring = str(message, 'ascii', 'replace')
            mstring = mstring[4:]
            met = message[4:]
            if addr[1] != servport:
                clientSocket.sendto(errorpack(5), addr)
                message, addr = clientSocket.recvfrom(516)
                mstring = str(message, 'ascii', 'replace')
                mstring = mstring[4:]
                met = message[4:]

            fillet.write(met)

            file_str += mstring

            if message[1] != 3 or len(message) < 512:
                isData = False
        print(file_str[2])
        fillet.close()

    elif mode == "w":
        fillet = open(filename, "r")
        if fillet.mode != 'r':
            return
        text = str(fillet.read())
        length = 512
        data_list = list(text[0 + i:length + i] for i in range(0, len(text), length))
        pack = write(filename)
        clientSocket.sendto(pack, serverAdd)
        message, addr = clientSocket.recvfrom(516)
        if message[1] == 5:
            exit()
        elif message[2] != 0 or message[3] != 0:
            print('No ack')

        block_num1 = 0
        block_num2 = 0

        for data in data_list:
            clientSocket.sendto(datapack(block_num1, block_num2, data), serverAdd)
            message, addr = clientSocket.recvfrom(516)
            if addr[1] != servport:
                clientSocket.sendto(errorpack(5), addr)
                message, addr = clientSocket.recvfrom(516)
            block_num1 = message[2]
            block_num2 = message[3]
            if message[1] == 5:
                sys.exit()
        exit()
    else:
        exit()
    clientSocket.close()

def read(filename):
    pack = bytearray()
    pack.append(0)
    pack.append(1)
    filename = bytearray(filename.encode('utf-8'))
    pack += filename
    pack.append(0)
    m = bytearray(bytes('netascii', 'utf-8'))
    pack += m
    pack.append(0)
    return pack

def write(filename):
    pack = bytearray()
    pack.append(0)
    pack.append(2)
    filename = bytearray(filename.encode('utf-8'))
    pack += filename
    pack.append(0)
    m = bytearray(bytes('netascii', 'utf-8'))
    pack += m
    pack.append(0)
    return pack

def datapack(ack, ack2, data):
    req = bytearray()
    req.append(0)
    req.append(3)
    a1 = ack
    a2 = ack2 + 1
    if a2 > 255:
        a2 = 0
        a1 = ack + 1
    req.append(a1)
    req.append(a2)
    req += bytearray(data.encode('ascii'))
    return req

def errorpack(error):
    req = bytearray()
    req.append(0)
    req.append(5)
    req.append(0)
    req.append(error)
    req += bytearray('This is an error.'.encode('utf-8'))
    req.append(0)
    return req

def ack(ack, ack2):
    ackno = bytearray()
    ackno.append(0)
    ackno.append(4)
    ackno.append(ack)
    ackno.append(ack2)
    return ackno

main()

