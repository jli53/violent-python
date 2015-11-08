#!/usr/bin/python
import sys
import zipfile
from threading import Thread

def test_pass(zFile, password):
  try:
    zFile.extractall(pwd=password)
    print '[+] Found password' + password + '\n'
  except:
    pass
'''
  f_zip = zipfile.ZipFile(filename)
  passfile = open("/usr/share/wordlists/rockyou.txt","r")
  for password in passfile.readlines():
    password = password.strip('\n')
    #password = "1234"
    try:
      print "trying " + password
      f_zip.extractall(pwd = password)
      print "[+] Password FOUND!!! It is " + password + "\n"
      return
    except Exception, e:
      #print e
      pass
  print "[-] NOT FOUND!" 
'''
def main():
  if len(sys.argv) != 2:
    print "[-] Usage: " + sys.argv[0] + " zipfilename"
    exit(0)
  else:
    zFile = zipfile.ZipFile(sys.argv[1])
    passfile = open("/usr/share/wordlists/rockyou.txt","r")
    for line in passfile.readlines():
      password = line.strip('\n')
      t = Thread(target=test_pass, args=(zFile, password))
      t.start()
main()
