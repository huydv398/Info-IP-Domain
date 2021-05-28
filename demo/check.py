import shodan
import requests
import telebot
import re
import json
import config
import sys
import ipaddress # Check ip
from bs4 import BeautifulSoup
from tldextract import tldextract

bot = telebot.TeleBot(config.TOKEN)
api = shodan.Shodan(config.API_SHODAN) 

# Reply hướng dẫn
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, """Nhập vào `/port <IP>` để xem port. VD: `/port 8.8.8.8`\nNhập vào `/domain`, `/Domain`, `/DOMAIN` `<domain>` để xem info của Domain. VD: `/domain onedata.vn`\n `/ip_rev` <ip> """, parse_mode='Markdown')
@bot.edited_message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, """Nhập vào `/port <IP>` để xem port. VD: `/port 8.8.8.8`\nNhập vào `/domain`, `/Domain`, `/DOMAIN` `<domain>` để xem info của Domain. VD: `/domain onedata.vn`\n `/ip_rev` <ip> """, parse_mode='Markdown')

# Hàm dùng để kiểm tra địa chỉ IP sử dụng module shodan API
def list_port(ipaddr):

    ipinfo= api.host(ipaddr)
    info = ipinfo['data']
    info_port = 'Port \tProtocol\tService'
    try:
        for data in info:
            port = str(data['port'])
            service = str(data['_shodan']['module'])
            protocol = str(data['transport'])
            inf_output = port + ': \t' +protocol+'\t\t'+ service 
            info_port = str(info_port +'\n'+ inf_output)

    except:
        info_port = 'Lỗi port'
        return info_port  
# Kiểm tra trạng thái và SSL. Sử dụng 
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
                out = str(name1[value]).ljust(25) + str(Info_domain.get(value).rjust(5) )
                list_in = list_in + str(out) + '\n'
            return list_in
        except:
            return ('Không có thông tin về tên miền vừa nhập')
    else:
        return 'Chưa điền Domain hoặc không phải là một Domain'
if __name__ == "__main__":
    # Tạo lệnh check port 
    @bot.message_handler(commands=["port"])
    def check_port(message):
        IP = message.text[6:]
        try:
            if ipaddress.ip_address(IP).is_private == False :
                port = list_port(IP)
                string_port  = str(port)
                send_message = bot.reply_to(message, IP + ' is IP Public' +'\n'+string_port, parse_mode='Markdown')
            elif ipaddress.ip_address(IP).is_private == True :
                send_message = bot.reply_to(message, IP + 'is IP Private', parse_mode='Markdown')
        except:
            end_message = bot.reply_to(message,  'None Infomation:' + IP, parse_mode='Markdown')
    @bot.message_handler(commands=["domain", "Domain", "DOMAIN", "p"])
    def check_port(message):
        input = message.text[7:]
        output_tele = info_domain(input)
        send_message = bot.reply_to(message, output_tele, parse_mode='Markdown')
    @bot.edited_message_handler(commands=["domain", "Domain", "DOMAIN"])
    def check_port(message):
        input = message.text[7:]
        output_tele = info_domain(input)
        send_message = bot.reply_to(message, output_tele, parse_mode='Markdown')
    @bot.edited_message_handler(commands=["port"])
    def check_port(message):
        IP = message.text[6:]
        try:
            if ipaddress.ip_address(IP).is_private == False :
                port = list_port(IP)
                string_port  = str(port)
                send_message = bot.reply_to(message, IP + ' is IP Public' +'\n'+string_port, parse_mode='Markdown')
            elif ipaddress.ip_address(IP).is_private == True :
                send_message = bot.reply_to(message, IP + 'is IP Private', parse_mode='Markdown')
        except:
            end_message = bot.reply_to(message, 'None Infomation:' + IP, parse_mode='Markdown')

    # Tạo lệnh check port 
    @bot.message_handler(commands=["ip_rev"])
    def test(message):
        IP = message.text[8:]
        try:
            if ipaddress.ip_address(IP).is_private == False :
                try : 
                    request.get("https://api.hackertarget.com/dnslookup/?q=hackertarget.com&apikey=plmoknijbuhvygvtrgedsfghhhhkjhkhfsk")
                    req= requests.get("https://api.hackertarget.com/reverseiplookup/?q={}".format(IP))
                    site = req.text
                except: 
                    site = "Hết lượt truy xuất !!"
                mess = str(site)

                if len(mess) > 4096: 
                    for x in range(0, len(mess), 4096):
                        send_message = bot.reply_to(message, mess[x:x+4096] , parse_mode='Markdown')
                else:
                    send_message = bot.reply_to(message, IP + ' '  + mess  , parse_mode='Markdown')
            elif ipaddress.ip_address(IP).is_private == True :
                send_message = bot.reply_to(message, IP + 'is IP Private' , parse_mode='Markdown')
        except:
            send_message = bot.reply_to(message, 'None Infomation:' , parse_mode='Markdown')
    @bot.edited_message_handler(commands=["ip_rev"])
    def test(message):
        IP = message.text[8:]
        try:
            if ipaddress.ip_address(IP).is_private == False :
                try : 
                    req= requests.get("https://api.hackertarget.com/reverseiplookup/?q={}".format(IP))
                    site = req.text
                except: 
                    site = "Hết lượt truy xuất !!"
                    print (site)
                mess = str(site)

                if len(mess) > 4096: 
                    for x in range(0, len(mess), 4096):
                        send_message = bot.reply_to(message, mess[x:x+4096] , parse_mode='Markdown')
                else:
                    send_message = bot.reply_to(message, IP + ' '  + mess  , parse_mode='Markdown')
            elif ipaddress.ip_address(IP).is_private == True :
                send_message = bot.reply_to(message, IP + 'is IP Private' , parse_mode='Markdown')
        except:
            send_message = bot.reply_to(message, 'None Infomation:' , parse_mode='Markdown')

    bot.polling()
