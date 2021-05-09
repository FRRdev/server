import smtplib, sys, email.utils, mailconfig

def send_message():
    ''' function for sending messages over smtp protocol '''
    mailserver = mailconfig.smtpservername
    From = input('From? ').strip()
    To = input('To? ').strip()
    Tos = To.split(';')
    Subj = input('Subj? ').strip()
    Date = email.utils.formatdate()
    # standard headers followed by an empty string and text
    text = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n' % (From, To, Date, Subj))
    print('Type message text, end with line=Ctrl+z (Windows)')
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        text += line
    print('Connecting...')
    server = smtplib.SMTP_SSL(mailserver, '465')
    server.login('your_email', 'password')
    failed = server.sendmail(From, Tos, text)
    server.quit()
    if failed:  # smtplib can raise exceptions
        print('Failed recipients:', failed)
    else:
        print('No errors.')
    print('Bye.')
