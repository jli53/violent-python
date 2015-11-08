#!/usr/bin/python

import optparse
import sys
from threading import *
from socket import *

def main():
  parser = optparse.OptionParser(usage="Usage: " + sys.argv[0] + " -H <host> -P <port[s]>")

  parser.add_option("-H", dest="tgt_host", type="string", help="target host")
  parser.add_option("-P", dest="tgt_port", type="string", help="target port number[s] separated by comma")

  (options, args) = parser.parse_args()

  tgt_host = options.tgt_host
  tgt_ports = str(options.tgt_port).split(",")

  if (tgt_host is None) | (tgt_ports is None):
    print parser.usage
    exit(0)
  else:
    portScan(tgt_host,tgt_ports)

#resolve host and call connScan
def portScan(tgt_host,tgt_ports):
  try:
    tgt_IP = gethostbyname(tgt_host)
  except Exception, e:
    print "[-]cannot resolve %s, unknow host" %tgt_host
    return

  try:
    tgt_name = gethostbyaddr(tgt_IP)
    print "Scan result for " + tgt_name[0] + ":"
  except:
    print "Scan result for " + tgt_IP + ":"

  for port in tgt_ports:
    t = Thread(target=connScan,args=(tgt_host, int(port)))
    t.start()

#actul connection scann
screenLock = Semaphore(value=1)
def connScan(tgt_host, port):
  try:
    connsk = socket(AF_INET, SOCK_STREAM)
    connsk.connect((tgt_host, port))
    connsk.send("hey yo\n")
    banner = connsk.recv(100)
    screenLock.acquire()
    print '[+]%d/tcp open: %s' %(port, str(banner).strip('\n'))
  except:
    screenLock.acquire()
    print '[-]%d/tcp closed' %port 
  finally:
    screenLock.release()
    connsk.close()

main()
