# -*- coding: utf-8 -*-
"""
Update DNSPOD DDNS IP (python 2.7)
    Create by Zong-Sheng Wang 
    @ 2018/01/13

if you wanna execute this script per hour:
crontab -e
1 */1 * * * /usr/bin/python /home/pi/update_ip.py >> /home/pi/update_ip.log

crontab -l
"""

import urllib
import urllib2
import re
import socket
import json
import sys 
import time

BASE_URL = 'https://api.dnspod.com'  # https://dnsapi.cn 


def GetIP():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip

def RequestApi(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    content = response.read()
    return json.loads(content)
    
    
def GetUserToken(email, password):
    url = BASE_URL + '/Auth'
    data = urllib.urlencode({'login_email': email, 'login_password': password, 
                             'format': 'json'})
    content_dict = RequestApi(url, data)
    if content_dict['status']['code'] == '1':
        return content_dict['user_token']
    else:
        return ""
    
def GetDomainID(token, domain):
    url = BASE_URL + '/Domain.List'
    data = urllib.urlencode({'user_token':token, 'format': 'json'})
    content_dict = RequestApi(url, data)
    domains_list = content_dict['domains']
    domain_id  = -1
    if content_dict['status']['code'] == '1':
        for domain_info in domains_list:
            if domain_info['name'] == domain:
                domain_id = domain_info["id"] 
   
    return domain_id


def GetRecordInfo(token, domain_id, record):
    url = BASE_URL + '/Record.List'
    data = urllib.urlencode({'user_token': token, 'domain_id': domain_id,
                             'format': 'json'})
    content_dict = RequestApi(url, data)
    records_list = content_dict['records']
    record_id  = -1
    if content_dict['status']['code'] == '1':
        for record_info in records_list:
            if record_info['name'] == record:
                record_id = record_info["id"] 
               
    return record_id

def UpdateDDNS(token, domain_id, record_id, record_line, sub_domain):
    url = BASE_URL + '/Record.Ddns'
    data = urllib.urlencode({'user_token': token, 'domain_id': domain_id,
                             'record_id': record_id, 'sub_domain': sub_domain,
                             'record_line': record_line, 
                             'format': 'json'})
    content_dict = RequestApi(url, data)
    return content_dict
    
    
    

if __name__ == '__main__':
    #myip = GetIP() 
    #print myip
    
    domain = 'yourdomain.com'
    record = 'your subdomain like (www)'
    email = 'your ddns account'
    password = 'your ddns password'
    
    token = GetUserToken(email, password)
    #print token
    if token == "":
        print "GetUserToken Error"
        sys.exit(0)
        
    
    domain_id = GetDomainID(token, domain)
    #print domain_id
    if domain_id == -1:
        print "GetDomainID Error"
        sys.exit(0)
        
    record_id = GetRecordInfo(token, domain_id, record)
    #print record_id
    if record_id == -1:
        print "GetRecordID Error"
        sys.exit(0)
        
    result = UpdateDDNS(token, domain_id, record_id, 'default', record)
    if result['status']['code'] == '1':
        print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))  
        print "%s.%s => %s\n" % (result['record']['name'], domain, result['record']['value'])

 
