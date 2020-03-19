#!/usr/bin/env python3

import sys
import socket
import re
import ipaddress
import argparse


parser = argparse.ArgumentParser(description = "Take hostnames on stdin and return IPs.")
parser.add_argument('-v', '--verbose', default=False, action="store_true", help="Set this to return both the hostname and ip.")
args = parser.parse_args()
verbose = args.verbose


def read_in():
	return [x.strip() for x in sys.stdin.readlines()]

def strip_prot(hostname):
	# remove protocol handler
	return hostname.split("//")[1] if "//" in hostname else hostname

hosts = read_in()

host_objs = []

for host in hosts:
	# TODO: This won't do ipv6 so we need a better solution
	try:
		host_objs.append(socket.gethostbyname_ex(strip_prot(host)))
	except:
		continue

if verbose:
	# if verbose is on then we output each host with its corresponding ip
	for host_obj in host_objs:
		for addr in host_obj[2]:
			print("{} {}".format(addr, host_obj[0]))
else:
	# otherwise we remove dupes and output just a list of ips. 
	addr_list = []
	for host_obj in host_objs:
		for addr in host_obj[2]:
			addr_list.append(addr)

	for i in list(set(addr_list)):
		print(i)
