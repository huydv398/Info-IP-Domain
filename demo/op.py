import shodan
import requests
import telebot
import re
import json
import config
import sys
import ipaddress 
domain = 'duonghuy.vn'
try:
    url1 = 'https://' + domain
    response = requests.get(url1)
    sta = response.status_code
    status = str(sta)
    status_domain= "Status code: " + status + ". Web có SSL."
except:
    url1 = 'http://' + domain
    response = requests.get(url1)
    sta = response.status_code
    status = str(sta)
    status_domain = "Status code: " + status + ". Web không có SSL."
        