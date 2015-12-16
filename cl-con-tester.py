#!/usr/bin/env python
#-*- coding: utf8 -*-
# Copyright © 2014 Denis Khabarov
import sys
from urllib2 import urlopen, URLError
from subprocess import Popen, PIPE
try:
        from ipaddr import IPAddress, IPNetwork
except ImportError, err_msg:
        print "%s\nTry 'pip install ipaddr'" % err_msg
        sys.exit(1)


def get_cloud_flare_ipv4_networks():
        print "\033[1mПолучение списка сетей CloudFlare\033[0m..."
        try:
                data = urlopen('https://www.cloudflare.com/ips-v4', timeout=5)
        except URLError, e:
                print "\033[31mError:\033[0m",e.reason
                sys.exit(1)
        else:
                return data.readlines()

def get_netstat():
        print "\033[1mПолучение текущих ESTABLISHED соединений...\033[0m"
        shell="netstat -utpn | grep '"+sys.argv[1]+"' | grep ESTABLISHED|awk -F ':' '{print $2}'|awk '{print $2}'"
        child = Popen(shell, shell = True, stdout=PIPE, stderr=PIPE, stdin=None)
        streamdata = child.communicate()
        return "".join(map(str, streamdata))

def main():
        try:
                sys.argv[1]
        except IndexError:
                print "\033[31mError! Example usage "+sys.argv[0]+" 127.0.0.1:80 \033[0m"
                sys.exit(1)
        cloud_flare_ips = 0
        non_cloud_flare_ips = 0
        networks = get_cloud_flare_ipv4_networks()
        print "\033[1mВычисление IP адресов...\033[0m"
        for ip in get_netstat().splitlines():
                if ip == '':
                        continue
                if [network for network in networks if IPAddress(ip.replace('\n','')) in IPNetwork(network.replace('\n',''))]:
                        cloud_flare_ips = cloud_flare_ips + 1
                else:
                        non_cloud_flare_ips = non_cloud_flare_ips + 1
        print "\033[1mResult:\033[0m"
        print "\t\033[32mCloudFlare Connections:\033[0m",cloud_flare_ips
        print "\t\033[31mNon CloudFlare Connections:\033[0m", non_cloud_flare_ips
        print "\t\033[1mTotal:\033[0m", cloud_flare_ips+non_cloud_flare_ips

if __name__ == '__main__':
        try:
                main()
        except KeyboardInterrupt:
                print "Rcv SIGINT. Exit..."
                exit(1)
