import requests
import re
import argparse
import urllib.request
import socket
import urllib.error
import time
import threading
from multiprocessing.dummy import Pool as ThreadPool
import os
working=0
checked=0
proxy_type=""		
def get_proxies(link):
	resp=requests.get(link)
	data=resp.text
	return data

def thread_test(proxy):
	global working
	global checked
	checked+=1			
	with open("working_proxies.txt",'a')as file:
		if is_good_proxy(proxy):
			global working;
			working+=1
			file.write('{0}\n'.format(proxy))
			print('Checked : [%d] Working : [%d]\r'%(checked,working), end="")	
			

def scrape(typ,link,test=False):
	global proxy_type
	proxy_type=typ
	for i in link.keys():
		temp=link[i]
		with open("proxies.txt",'a')as file:
			data=get_proxies(temp)
			data=data.split('\r\n')
			print("Total no of proxies : ",len(data))
			for i in data:
				file.write('{0}\n'.format(i))
			print("All proxies are stored in proxies.txt")
			if test:
				checked=0
				print("Checking Proxies")
				
				pool=ThreadPool(20)
				results = pool.map(thread_test, data)
				pool.close()
				pool.join()
			
				
			print("Total no of working proxies : ",working)
	print("COMPLETED!!!!! @r4ge")

def banner():
	print('''
	  ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███  ▓█████ 
▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓█   ▀ 
░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▒███   
  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒▓█  ▄ 
▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░░▒████▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░░░ ▒░ ░
░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░      ░ ░  ░
░  ░  ░  ░          ░░   ░   ░   ▒   ░░          ░   
      ░  ░ ░         ░           ░  ░            ░  ░
         ░                                           
	  _____      ____         
 / ___ \____/ / /___ ____ 
/ / _ `/ __/_  _/ _ `/ -_)
\ \_,_/_/   /_/ \_, /\__/ 
 \___/         /___/      
	
	''')
def main():
	socket.setdefaulttimeout(120)
	banner()
	parser=argparse.ArgumentParser()
	parser.add_argument("type",help='''Scrape proxies
										http ,
										socks4 ,
										socks5				
	''')
	parser.add_argument("-c",help="pass true or false to check")
	args = parser.parse_args()
	proxy_type="";
	api_link={1:'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'}
	if args.type=='http':
		print("Scraping http poxies")
		proxy_type='http'
		#api_link[1]=api_link[1].replace("type=undefined","type=http")
	elif args.type=='socks4':
		print("scraping socks4 proxies")
		proxy_type='socks4'
		#api_link[1]=api_link[1].replace("type=undefined","type=socks4")
		api_link[1]=api_link[1].replace("protocol=http","protocol=socks4")
	elif args.type=='socks5':
		print('scraping socks5 proxies')
		proxy_type='socks5'
		#api_link[1]=api_link[1].replace("type=undefined","type=socks5")
		api_link[1]=api_link[1].replace("protocol=http","protocol=socks5")
	else:
		print("Unknow Type")
		print(parser.print_help())
	if os.path.isfile("proxies.txt"):
		print()
		chk=input("Warning!! proxies.txt file alread exists you want to remove or continue[y/n]")
		if chk.lower()=='y':
			os.remove('proxies.txt')
		else:
			print("Will append the output in the same file!!!")
	if args.c is not False:
		if proxy_type!='http':
			print("Checking For now is sonly supported for http")
			print(parser.print_help())
			exit
		if os.path.isfile("working_proxies.txt"):
			print()
			chk=input("Warning!! working_proxies.txt file alread exists you want to remove or continue[y/n]")
			if chk.lower()=='y':
				os.remove('working_proxies.txt')
		else:
			print("Will append the output in the same file!!!")
		scrape(proxy_type,api_link,True)
	else:
		scrape(proxy_type,api_link)
def is_good_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('http://www.google.com')  # change the URL to test here
        sock=urllib.request.urlopen(req,timeout=10)
    except urllib.error.HTTPError as e:
        return False
    except Exception as detail:
        return False
    return True

if __name__=="__main__":
	main()
