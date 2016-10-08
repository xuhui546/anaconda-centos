import string
import argparse
import os,sys,re,subprocess
from random import choice
from IPython.lib import passwd

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)
parser.add_argument("-n", "--confname", help="set ipython config folder name(default:mynbs)", action="store", default='mynbs')
parser.add_argument("-p", "--password", help="set ipython login password(default:random)", action="store")
parser.add_argument("-l", "--listen", help="set ipython server listen port(default:8888)", type=int, action="store", default=8888)
args = parser.parse_args()

# set argument
iPort = args.listen
bVerbose = args.verbose
sConfName = args.confname
sHome = os.path.expanduser('~')
sPath = sHome+'/.ipython/profile_{}/'.format(sConfName)
sFilename = 'ipython_notebook_config.py'

if os.path.exists(sPath):
    print(sPath + ' already exists.\nexit configure.')
    sys.exit()

# set ipython notebook login password
sPassword = args.password or ''.join([choice(string.ascii_letters+string.digits) for i in range(8)])
sSha1 = passwd(sPassword)


# create ipython profile
s = subprocess.Popen('ipython profile create {}'.format(sConfName), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
o = s.communicate()
bVerbose and print(o[0].decode())
bVerbose and print(o[1].decode())

# create private key and certificate
s = subprocess.Popen("""
openssl req -x509 -nodes -days 1000 -newkey rsa:1024 -keyout {sHome}/mycert.pem -out {sHome}/mycert.pem <<EOF







EOF
""".format(sHome=sHome), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
bVerbose and print('create private key and certificate in {}'.format(sHome))

# set ipython notbook file
with open(sPath+sFilename, 'w+') as f:
    f.write("""\n
#### Modify ipython_notebook_config.py configuration file
#### Add these lines to the top of the file; no other changes necessary
#### Obviously, you'll want to add your path to the .pem key and your password

# Configuration file for ipython-notebook.

c = get_config()

# Kernel config
c.IPKernelApp.pylab = 'inline'  # if you want plotting support always

c.NotebookApp.certfile = u'{}/mycert.pem'
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.password = u'{}'
# It is a good idea to put it on a known, fixed port
c.NotebookApp.port = {}
""".format(sHome, sSha1, iPort))
bVerbose and print('{} has configured in {}'.format(sFilename, sPath))

print("""
============================================================
Notebook config path: {}
Notebook certificate path: {}
Notebook password: {}
Notebook port: {}
============================================================
""".format(sPath, sHome, sPassword, iPort))





