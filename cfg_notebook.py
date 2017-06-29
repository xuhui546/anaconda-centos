import string
import argparse
import os,sys,re,subprocess
from random import choice
from IPython.lib import passwd

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)
parser.add_argument("-p", "--password", help="set ipython login password(default:random)", action="store")
parser.add_argument("-l", "--listen", help="set ipython server listen port(default:8888)", type=int, action="store", default=8888)
args = parser.parse_args()

# set argument
iPort = args.listen
bVerbose = args.verbose
sPath = os.path.expanduser('~') + '/.jupyter/'
sFilename = 'jupyter_notebook_config.py'

if os.path.exists(sPath):
    print(sPath + ' already exists.\nexit configure.')
    sys.exit()

# set ipython notebook login password
sPassword = args.password or ''.join([choice(string.ascii_letters+string.digits) for i in range(8)])
sSha1 = passwd(sPassword)


# create ipython profile
s = subprocess.Popen('jupyter notebook --generate-config', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
o = s.communicate()
bVerbose and print(o[0].decode())
bVerbose and print(o[1].decode())

# create private key and certificate
s = subprocess.Popen("""
openssl req -x509 -nodes -days 1000 -newkey rsa:1024 -keyout {sPath}mykey.key -out {sPath}mycert.pem <<EOF







EOF
""".format(sPath=sPath), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
bVerbose and print('create private key and certificate in {}'.format(sPath))

# set ipython notbook file
with open(sPath+sFilename, 'w+') as f:
    f.write("""\n
#### Modify ipython_notebook_config.py configuration file
#### Add these lines to the top of the file; no other changes necessary
#### Obviously, you'll want to add your path to the .pem key and your password

## The full path to an SSL/TLS certificate file.
c.NotebookApp.certfile = u'{sPath}mycert.pem'

## The IP address the notebook server will listen on.
c.NotebookApp.ip = '*'

## The full path to a private key file for usage with SSL/TLS.
c.NotebookApp.keyfile = u'{sPath}mykey.key'

c.NotebookApp.password = u'{sSha1}'

c.NotebookApp.open_browser = False

## The port the notebook server will listen on.
c.NotebookApp.port = {iPort} 

""".format(sPath=sPath, sSha1=sSha1, iPort=iPort))
bVerbose and print('{} has configured in {}'.format(sFilename, sPath))

print("""
============================================================
Notebook config path: {}
Notebook certificate path: {}
Notebook password: {}
Notebook port: {}
============================================================
""".format(sPath, sPath, sPassword, iPort))
