#!/usr/bin/python

import nmap
import optparse
import sys

def portScanner(tgt_host, tgt_port):
  nmscan = nmap.PortScanner()
  result = nmscan.scan(tgt_host,tgt_port)
  state = result['scan'][tgt_host]['tcp'][int(tgt_port)]['state']
  print '[*]' + tgt_host + ' tcp/' + tgt_port + ': ' + state

def main():
  parser = optparse.OptionParser('Usage: '+sys.argv[0]+' -H <host> -P <port[s]>')
  parser.add_option('-H', dest='tgt_host', type='string',  help='target host')
  parser.add_option('-P', dest='tgt_ports', type='string',  help='target ports, separated by comma')

  options, args = parser.parse_args()

  tgt_host = options.tgt_host
  tgt_ports = str(options.tgt_ports).split(',')

  if (tgt_host is None) | (tgt_ports is None):
    print parser.usage
    exit(0)
  else:
    for port in tgt_ports:
      portScanner(tgt_host, port)

main()
