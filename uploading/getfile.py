import sys, os, time, _thread as thread
from socket import *
from os.path import exists
from ftplib import FTP

blksz = 1024
defaultHost = 'localhost'
defaultPort = 50001

helptext = """
Usage...
server=> getfile.py -mode server [-port nnn] [-host hhh|localhost]
client=> getfile.py [-mode client] -file fff [-port nnn] [-host
hhh|localhost]
"""


def now():
    return time.asctime()


def parsecommandline():
    dict = {}
    args = sys.argv[1:]
    while len(args) >= 2:
        dict[args[0]] = args[1]
        args = args[2:]
    return dict


def client(host, port, filename):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    sock.send((filename + '\n').encode())
    dropdir = os.path.split(filename)[1]
    file = open(dropdir, 'wb')
    while True:
        data = sock.recv(blksz)
        if not data: break
        file.write(data)
    sock.close()
    file.close()
    print('Client got', filename, 'at', now())


def serverthread(clientsock):
    sockfile = clientsock.makefile('r')  # wrap a socket with a file object
    filename = sockfile.readline()[:-1]  # get the file name
    try:
        file = open(filename, 'rb')
        while True:
            bytes = file.read(blksz)
            if not bytes: break
            sent = clientsock.send(bytes)
            assert sent == len(bytes)
    except:
        print('Error downloading file on server:', filename)
    clientsock.close()


def server(host, port):
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.bind((host, port))
    serversock.listen(5)
    while True:
        clientsock, clientaddr = serversock.accept()
        print('Server connected by', clientaddr, 'at', now())
        thread.start_new_thread(serverthread, (clientsock,))


def main(args):
    host = args.get('-host', defaultHost)
    port = int(args.get('-port', defaultPort))
    if args.get('-mode') == 'server':  # None, if not-mode: client
        if host == 'localhost': host = ''
        server(host, port)
    elif args.get('-file'):
        client(host, port, args['-file'])
    else:
        print(helptext)


def getfile(file, site, dir, user=(), *, verbose=True, refetch=False):
    ''' Getting from the server over ftp'''
    if exists(file) and not refetch:
        if verbose: print(file, 'already fetched')
    else:
        if verbose: print('Downloading', file)
        local = open(file, 'wb')
        try:
            remote = FTP(site)  # connect to an FTP site
            remote.login(*user)  # for anonymous = () or (name, password)
            remote.cwd(dir)
            remote.retrbinary('RETR ' + file, local.write, 1024)
            remote.quit()
        finally:
            local.close()
        if verbose: print('Download done.')


if __name__ == '__main__':
    args = parsecommandline()
    main(args)
