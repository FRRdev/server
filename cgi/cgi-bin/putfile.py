import cgi, os, sys, html as ht
import posixpath, ntpath  # to handle client paths

debugmode = False  # True=output of form data
loadtextauto = False  # True=read the entire file
uploaddir = './uploads'  # directory for saving files
sys.stderr = sys.stdout
form = cgi.FieldStorage()
print("Content-type: text/html\n")
if debugmode: cgi.print_form(form)
html = """
<html><title>Putfile response page</title>
<body>
<h1>Putfile response page</h1>
%s
</body></html>"""
goodhtml = html % """
<p>Your file, '%s', has been saved on the server as '%s'.
<p>An echo of the file's contents received and saved appears below.
</p><hr>
<p><pre>%s</pre>
</p><hr>
"""


def splitpath(origpath):  # get file name without path
    for pathmodule in [posixpath, ntpath]:  # check all types
        basename = pathmodule.split(origpath)[1]
        if basename != origpath:
            return basename
    return origpath


def saveonserver(fileinfo):
    basename = splitpath(fileinfo.filename)
    srvrname = os.path.join(uploaddir, basename)
    srvrfile = open(srvrname, 'wb')
    if loadtextauto:
        filetext = fileinfo.value  # read the text in a line
        if isinstance(filetext, str):
            filedata = filetext.encode()
            srvrfile.write(filedata)
    else:  # otherwise read line by line
        numlines, filetext = 0, ''
        while True:
            line = fileinfo.file.readline()
            if not line: break
            if isinstance(line, str):
                line = line.encode()
            srvrfile.write(line)
            filetext += line.decode()
            numlines += 1
        filetext = ('[Lines=%d]\n' % numlines) + filetext
    srvrfile.close()
    os.chmod(srvrname, 0o666)  # allow entry: owner of 'nobody'
    return filetext, srvrname


def main():
    if not 'clientfile' in form:
        print(html % 'Error: no file was received')
    elif not form['clientfile'].filename:
        print(html % 'Error: filename is missing')
    else:
        fileinfo = form['clientfile']
        try:
            filetext, srvrname = saveonserver(fileinfo)
        except:
            errmsg = '<h2>Error</h2><p>%s<p>%s' % tuple(sys.exc_info()[:2])
            print(html % errmsg)
        else:
            print(goodhtml % (ht.escape(fileinfo.filename), ht.escape(srvrname), ht.escape(filetext)))


main()
