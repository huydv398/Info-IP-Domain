import shodan
import requests
import telebot
import re
import json
import config
import sys
import ipaddress 

def info_domain(input):
    pattern = '^([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}$'
    domain2 = input.replace(" ", "" )
    domain1 = domain2.replace("www.", "" )
    domain = domain1.replace("WWW.", "" )

    if re.match(pattern, domain) :
        try:    
            try:
                url1 = 'https://' + domain
                response = requests.get(url1)
                sta = response.status_code
                status = str(sta)
                status_domain= "Status code: " + status + ". Web có SSL."
                # return status_domain
            except:
                url1 = 'http://' + domain
                response = requests.get(url1)
                sta = response.status_code
                status = str(sta)
                status_domain = "Status code: " + status + ". Web không có SSL."
                # return status_domain
            
            # Request API lấy IPS
            url_api = "https://checkport.p.rapidapi.com/"
            payload = {"format":"json","domain":"{}" .format(domain)}
            headers = {
                'x-rapidapi-host': "zozor54-whois-lookup-v1.p.rapidapi.com",
                'x-rapidapi-key': "6b52139521mshde1c8dd450b3d8fp1ee64fjsn34ae851601bc",
            }
            requests_info1 = requests.request("GET",url_api, params=payload, headers=headers)
            Info_domain1 = requests_info1.json()
            IPS = Info_domain1['ips']
            requests_info = requests.get("https://inet.vn/api/whois/{}".format(domain))
            Info_domain = requests_info.json() 
            name1 = { 'domainName' : 'Domain:' , 'registrantName' : 'Chủ sở hữu:', 'creationDate' :  'Ngày tạo:', 'expirationDate' : 'Ngày hết hạn:', 'nameServer' : 'Nameserver:', 'registrar' : 'Quản lý bởi Nhà đăng ký:' }
            list_in = status_domain +'\n'
            list_in = list_in +'IP: '+ IPS + '\n'
            for value in name1:
                out = str(name1[value]).ljust(15) + str(Info_domain.get(value))
                list_in = list_in + str(out) + '\n'
            return list_in
        except:
            return ('Không có thông tin về tên miền vừa nhập')
    else:
        status_domain = 'Chưa điền Domain hoặc không phải là một Domain'
        return status_domain
op = info_domain('onedata.vn')
print(op)
