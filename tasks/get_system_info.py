#!/usr/bin/python3
# Write a script that gets system information like:
#  distro info, 
#  memory(total, used, free), 
#  CPU info (model, core numbers, speed), 
#  current user, 
#  system load average, and 
#  IP address. 

# Possible options : -d, -m -c -u -l -i
import platform, re, logging, psutil, cpuinfo, os
from urllib import request
import argparse

def getPublicIp():
    data = str(request.urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

def getSystemInfo():
    try:
        info={}
        info['distro']=platform.version()
        info['architecture']=platform.machine()
        info['user']=os.environ.get('USER') if os.environ.get('USER') else os.environ.get('USERNAME') #psutil.users()
        info['ip-address']=getPublicIp()
        info['processor']=cpuinfo.get_cpu_info().get('brand_raw')
        info['proc-freq']=str(int(re.search(r'(\d+)', os.popen('sysctl hw.tbfrequency').read()).group()) / 1e7) + "GHz"
        info['proc-load']=psutil.cpu_percent()
        info['proc-load-avg']=psutil.getloadavg()
        info['proc-numb']=psutil.cpu_count()
        info['mem-total']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info['mem-used']=str(round(psutil.virtual_memory().used / (1024.0 **3)))+" GB"
        info['mem-free']=str(round(psutil.virtual_memory().free / (1024.0 **3)))+" GB"
        return info
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    systemInfo = getSystemInfo()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help = "Show distribution", action='store_true')
    parser.add_argument("-m", help = "Show memory", action='store_true')
    parser.add_argument("-c", help = "Show CPU", action='store_true')
    parser.add_argument("-u", help = "Show current user", action='store_true')
    parser.add_argument("-l", help = "Show load avg", action='store_true')
    parser.add_argument("-i", help = "Show ip address", action='store_true')

    args = parser.parse_args()

    if args.d:
        print(f"Distro: {systemInfo['distro']}")
    if args.m:
        print(f"Memory (total/free/used): {systemInfo['mem-total']} / {systemInfo['mem-free']} / {systemInfo['mem-used']}")
    if args.c:
        print(f"Processor: {systemInfo['processor']} {systemInfo['proc-freq']} Cores: {systemInfo['proc-numb']}")
    if args.u:
        print(f"Current user: {systemInfo['user']}")
    if args.l:
        print(f"Load average: {systemInfo['proc-load-avg']}")
    if args.i:
        print(f"External ip address: {systemInfo['ip-address']}")