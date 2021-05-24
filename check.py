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
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, """Nhập vào `/port <IP>` để xem port. VD: `/port 8.8.8.8`\nNhập vào `/domain`, `/Domain`, `/DOMAIN` `<domain>` để xem info của Domain. VD: `/domain onedata.vn`""", parse_mode='Markdown')
# @bot.message_handler()
# def echo_all(message):
# 	bot.reply_to(message, """Điều bạn nhập không phải là một câu lệnh\n`/start` hoặc `/help` để xem các lệnh sẵn có""", parse_mode='Markdown') 

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
    domain2 = input.replace(" ", "" )
    domain1 = domain2.replace("www.", "" )
    domain = domain1.replace("WWW.", "" )

    te_result = tldextract.extract(domain)
    domain1 = '{}.{}'.format(te_result.domain, te_result.suffix)
    func1 = (domain == domain1)

    if (func1 == False) :
        status_domain = 'Chưa điền Domain hoặc không phải là một Domain'
        return status_domain
    else:
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
            status_domain = "Status code: " + status + ". Web không có SSL.\n"
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
        IPS = str(Info_domain1['ips'])

        # Request API lấy infomation 
        requests_info = requests.get("https://inet.vn/api/whois/{}".format(domain))
        Info_domain = requests_info.json() 

        try:
            registrant = str(Info_domain['registrantName'])
            creation = str(Info_domain['creationDate'])
            expiration = str(Info_domain['expirationDate'])
            nameServer = str(Info_domain['nameServer'])
            # registrar = str(Info_domain['registrarName'])
        except: 
            registrant = 'None'
            creation = 'None'
            expiration = 'None'
            nameServer = 'None'
            nameserver = 'None'
            # registrar = 'None'
        list_in = status_domain + '\n'
        list_in = list_in + 'Domain: \t' + domain + '\n'
        list_in = list_in + 'IPS\t\t' + IPS + '\n'
        list_in = list_in + 'Chủ sở hữu:\t' + registrant + '\n'
        list_in = list_in + "Ngày tạo: \t" + creation + '\n'
        list_in = list_in + "Ngày hết hạn: \t" + expiration + '\n'
        list_in = list_in + "Nameserver: \t" + nameServer + '\n'
        # list_in = list_in + "Quản lý tại Nhà đăng ký: \t" + registrar + '\n \n'
        return list_in


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


    bot.polling()

