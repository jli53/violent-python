#!/usr/bin/python
import sys
import crypt
def testpass(passs):
  salt = passs[0:2]
  f = open("/usr/share/wordlists/rockyou.txt","r")
  for line in f.readlines():
    line = line.strip('\n')
    print "trying " + line
    new_pass = crypt.crypt(line,salt)
    if new_pass == passs:
      print "FOUND!!"
      return line
  return

def testsha512(ppass):
  salt = ppass.split("$")[2]
  hash_type = ppass.split("$")[1]
  if hash_type == '6':
    print "this is sha512"
  else:
    print "type is: " + hash_type
    return
  insalt = "$"+hash_type +"$"+salt+"$"

  f = open('/usr/share/wordlists/rockyou.txt','r')
  for line in f.readlines():
    line = line.strip('\n')
    print "trying: " + line
    new_pass = crypt.crypt(line,salt)
    if new_pass == ppass:
      print "[+] found!"
      return

  print "Not found"
  return

def main():
  if len(sys.argv) != 2:
    print "[-] Usage:" + sys.argv[0] + " <passwordfile>\nthis program uses kali password dictionary 'rockyou.txt'."
    exit(0)
  passfile = open(sys.argv[1],'r')
  for line in passfile.readlines():
    line = line.strip('\n')
    passs = line.split(":")[1]	
    if passs in ["*", "x", "!"]:
      print "skip this user"
    else:
      print "testing " + passs
      testsha512(passs)
  return
     
main()
