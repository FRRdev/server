import poplib, getpass, sys, mailconfig

port = "995"

def read_message():
    ''' Function for reading messages over the pop protocol '''
    mailserver = mailconfig.popservername
    mailuser = mailconfig.popusername
    mailpasswd = getpass.getpass('Password for %s?' % mailserver)
    print('Connecting...')
    server = poplib.POP3_SSL(mailserver,port)
    server.user(mailuser) # connection, registration on the server
    server.pass_(mailpasswd)
    try:
        print(server.getwelcome()) # output of the greeting
        msgCount, msgBytes = server.stat()
        print('There are', msgCount, 'mail messages in', msgBytes, 'bytes')
        print(server.list())
        print('-' * 80)
        input('[Press Enter key]')
        for i in range(msgCount):
            hdr, message, octets = server.retr(i+1)
            for line in message: print(line.decode())
            print('-' * 80)
            if i < msgCount - 1:
                input('[Press Enter key]')
    finally:
        server.quit()
    print('Bye.')
