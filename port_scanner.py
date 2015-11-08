#!/usr/bin/python
import sys
import os
import socket

def retBanner(ip, port):
  try:
    print "test"+ip+":"+str(port)
    socket.setdefaulttimeout(2)
    s = socket.socket()
    s.connect((ip, port))
    banner = s.recv(1024)
    print "test"+ip+":"+str(port)
    print banner
    return banner
  except:
    return

def checkVulns(banner, filename):
  f = open(filename, "r");
  for line in f.readlines():
    if line.strip("\n") in banner:
      print "[+] server is vulnerable:" + banner.strip("\n")

def main():
  if len(sys.argv) == 2:
    filename = sys.argv[1]
    if not os.path.isfile(filename):
      print "[-] " + filename + " does not exist"
      exit(0)
    if not os.access(filename, os.R_OK):
      print "[-] " + filename + " access denied."
      exit(0)

  else:
    print "[-]Usage " + str(sys.argv[0]) + " <vuln filename>.\nvuln file is used for store known vulnerable banners"
    exit(0)

  portList = [21,22,25,80,110,443]
  for x in range(142,144):
    ip = '192.168.1.' + str(x)
    for port in portList:
      banner = retBanner(ip, port)
      if banner:
        print '[+] ' + ip +": "+banner
	checkVulns(banner,filename)

if __name__ == '__main__':
  main()
