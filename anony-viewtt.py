import base64
from pystyle import *
import os
import sys
import ssl
import re
import time
import random
import threading
import requests
import hashlib
import json

from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

r = requests.Session()
r.cookies.set_policy(BlockCookies())

class Gorgon:
	def __init__(self,params:str,data:str,cookies:str,unix:int)->None:self.unix=unix;self.params=params;self.data=data;self.cookies=cookies
	def hash(self,data:str)->str:
		try:_hash=str(hashlib.md5(data.encode()).hexdigest())
		except Exception:_hash=str(hashlib.md5(data).hexdigest())
		return _hash
	def get_base_string(self)->str:base_str=self.hash(self.params);base_str=base_str+self.hash(self.data)if self.data else base_str+str('0'*32);base_str=base_str+self.hash(self.cookies)if self.cookies else base_str+str('0'*32);return base_str
	def get_value(self)->json:base_str=self.get_base_string();return self.encrypt(base_str)
	def encrypt(self,data:str)->json:
		unix=self.unix;len=20;key=[223,119,185,64,185,155,132,131,209,185,203,209,247,194,185,133,195,208,251,195];param_list=[]
		for i in range(0,12,4):
			temp=data[8*i:8*(i+1)]
			for j in range(4):H=int(temp[j*2:(j+1)*2],16);param_list.append(H)
		param_list.extend([0,6,11,28]);H=int(hex(unix),16);param_list.append((H&4278190080)>>24);param_list.append((H&16711680)>>16);param_list.append((H&65280)>>8);param_list.append((H&255)>>0);eor_result_list=[]
		for (A,B) in zip(param_list,key):eor_result_list.append(A^B)
		for i in range(len):C=self.reverse(eor_result_list[i]);D=eor_result_list[(i+1)%len];E=C^D;F=self.rbit_algorithm(E);H=(F^4294967295^len)&255;eor_result_list[i]=H
		result=''
		for param in eor_result_list:result+=self.hex_string(param)
		return{'X-Gorgon':'0404b0d30000'+result,'X-Khronos':str(unix)}
	def rbit_algorithm(self,num):
		result='';tmp_string=bin(num)[2:]
		while len(tmp_string)<8:tmp_string='0'+tmp_string
		for i in range(0,8):result=result+tmp_string[7-i]
		return int(result,2)
	def hex_string(self,num):
		tmp_string=hex(num)[2:]
		if len(tmp_string)<2:tmp_string='0'+tmp_string
		return tmp_string
	def reverse(self,num):tmp_string=self.hex_string(num);return int(tmp_string[1:]+tmp_string[:1],16)

def send(did, iid, cdid, openudid):
    global reqs, _lock, success, fails
    
    for x in range(10):
        try:
            params  = f"device_id={did}&iid={iid}&device_type=SM-G973N&app_name=musically_go&host_abi=armeabi-v7a&channel=googleplay&device_platform=android&version_code=160904&device_brand=samsung&os_version=9&aid=1340"
            payload = f"item_id={__aweme_id}&play_delta=1"
            sig     = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()

            response = requests.post(
                url = (
                    "https://api16-va.tiktokv.com/aweme/v1/aweme/stats/?" + params
                ),
                data    = payload,
                headers = {'cookie':'sessionid=90c38a59d8076ea0fbc01c8643efbe47','x-gorgon':sig['X-Gorgon'],'x-khronos':sig['X-Khronos'],'user-agent':'okhttp/3.10.0.1'},
                verify  = False
            )
            reqs += 1
            try:
                _lock.acquire()
                print(f"\033[1;31m[\033[1;34m {reqs}\033[1;31m ]\033[1;32m TĂNG VIEW THÀNH CÔNG\033[1;31m  | \033[1;97mID: {__aweme_id}\033[1;31m | \033[1;33m ĐÃ TĂNG: {reqs} VIEW\033[1;31m |")
                _lock.release()
                success += 1
            except:
                fails += 1
                continue

        except Exception as e:
            pass

def rpsm_loop():
    global rps, rpm
    while True:
        initial = reqs
        time.sleep(1.5)
        rps = round((reqs - initial) / 1.5, 1)
        rpm = round(rps * 60, 1)

def title_loop():
    global rps, rpm, success, fails, reqs
        
    if os.name == "nt":
        while True:
            time.sleep(0.1)

if __name__ == "__main__":  
    print(f''' 
      \033[1;35m █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗██╗   ██╗       
      \033[1;37m██╔══██╗████╗  ██║██╔═══██╗████╗  ██║╚██╗ ██╔╝       
      \033[1;35m███████║██╔██╗ ██║██║   ██║██╔██╗ ██║ ╚████╔╝        
      \033[1;37m██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║  ╚██╔╝         
      \033[1;35m██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║   ██║   
      \033[1;37m╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝
\033[1;31m────────────────────────────────────────────────────────────
\033[1;37m=> \033[1;37mTool: \033[1;33mBuff View Tik Tok Max Speed
\033[1;37m=> \033[1;34mAdmin: \033[1;31mPhan Gia Huy
\033[1;37m=> \033[1;35mYoutube:\033[1;32m Anony Coder
\033[1;37m=> \033[1;36mZalo: \033[1;31m0325380433
\033[1;37m=> \033[1;32mBox Suport: \033[1;37mhttps://zalo.me/g/aiddsu057 
\033[1;31m────────────────────────────────────────────────────────────''')
    try:
        link = str(Write.Input("[✓ ] Nhập Link Video Tik Tok: ", Colors.green_to_white, interval=0.0001))
        __aweme_id = str(
            re.findall(r"(\d{18,19})", link)[0]
            if len(re.findall(r"(\d{18,19})", link)) == 1
            else re.findall(
                r"(\d{18,19})",
                requests.head(link, allow_redirects=True, timeout=5).url
            )[0]
        )
    except:
        input(Col.red + "[*] Link Sai Rồi" + Col.reset)
        sys.exit(0)
    
    os.system("cls" if os.name == "nt" else "clear")
    
    _lock = threading.Lock()
    reqs = 0
    success = 0
    fails = 0
    rpm = 0
    rps = 0
    
    threading.Thread(target=rpsm_loop).start()
    threading.Thread(target=title_loop).start()

    devices = open('devices.txt', 'r').read().splitlines()
    while True:
        device = random.choice(devices)

        if eval("threading.active_count() < 100 # don't change count or u will kill devices and ruin fun for others"):
            did, iid, cdid, openudid = device.split(':')
            eval('threading.Thread(target=send,args=[did,iid,cdid,openudid]).start()')