import argparse
import os,re,subprocess
from IPython.lib import passwd

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)
parser.add_argument("-n", "--confname", help="set ipython config folder name(default:mynbs)", action="store", default='mynbs')
parser.add_argument("-i", "--password", help="set ipython config folder name(default:mypass)", action="store", default='mypass')
parser.add_argument("-p", "--port", help="set ipython config folder name(default:mypass)", type=int, action="store", default=8888)
args = parser.parse_args()

# set argument
bVerbose = args.verbose
sConfName = args.confname
# set ipython notebook login password
sPassword = passwd(args.password)
iPort = args.port

sHome=os.path.expanduser('~')
sPath=sHome+'/.ipython/profile_{}/'.format(sConfName)
sFilename='ipython_notebook_config.py'

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
""".format(sHome, sPassword, iPort))
bVerbose and print('{} has configured in {}'.format(sFilename, sPath))

