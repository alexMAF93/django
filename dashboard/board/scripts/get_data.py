#!/usr/local/bin/python3


from subprocess import Popen, PIPE
import os, sys, platform, re, requests, psutil


alarms = "" # string used to keep the alarms that will pop up after running the script
# The idea is to send an email if there are alarms for the server


def banner(n=60):
    print("="*n)
    print("=" + "=".rjust(n-1))
    print("=" + "=".rjust(n-1))
    print("=" + "Monitoring script".center(n-2) + "=")
    print("=" + "=".rjust(n-1))
    print("=" + "=".rjust(n-1))
    print("="*n)


def separate_sections(n=60):
    print('-'*n)
    
    
def format_output(str1, str2):
    """
    function that aligns 2 strings
    in 2 columns separated by a colon
    """
    print(str1.ljust(15), ':', str2.ljust(15))
    

def check_internet_connectivity(url='http://whatismyip.akamai.com'):
    """
    function that checks if there is 
    connectivity to internet.
    If there is, it gets the external
    IP
    """
    data = requests.head(url)
    page_content = requests.get(url)
    if data.status_code < 400:
        result = 'yes'
    else:
        result = 'no'
    format_output('Internet access', result)
    if result == 'yes':
        format_output('External IP', page_content.text)


def get_hardware_specs():
    """
    Function that gets some hardware
    specs of the server
    """
    cpu_info_file = open('/proc/cpuinfo', 'r')
    model_name = 'N/A'
    for line in cpu_info_file.readlines():
        if re.match('model name.*', line):
            model_name = re.sub('^\s', '', line.split(':')[1].replace('\n', ''))
            break
    cpu_info_file.close()

    with open('/etc/redhat-release') as dist_file:
        dist = dist_file.read()

    specs = {'Server\'s name': platform.node(),
    'System': platform.system(),
    'Distribution': dist.replace('\n',''),
    'Architecture': platform.machine(),
    'Release': platform.release(),
    'CPU Family': model_name,
    'CPUs': str(psutil.cpu_count()),
    'Frequency': str(psutil.cpu_freq(percpu=False).current),
    'Python Version': platform.python_version()
    } # the specs are in a dictionary
    # so that I can display the output
    # easier using a simple for loop
    
    for key, value in specs.items():
        format_output(key, value)

        
def get_ips():
    """
    function that gets the IP address
    for each interface of the server
    """
    print('Network Interfaces')
    # Unfortunately, it's not portable yet...
    ip_a = Popen(['ip', 'a'], stdout=PIPE)
    for bytes in ip_a.stdout:
        line = bytes.decode()
        if re.match('\s+inet ', line):
            ip_address = line.split()[1].split('/')[0]
            interface = line.split()[-1]
            format_output(interface, ip_address)

            
def get_virtual_memory_SWAP():
    """
    function that gets the virtual and
    swap memories.
    Also, it shows the free percentage
    for each of these.
    """
    global alarms
    Total_mem = psutil.virtual_memory().total / 1024 / 1024 # psutil gets these values in Bytes
    Used_mem = (psutil.virtual_memory().used / 1024 / 1024 ) * 100 / Total_mem
    Total_SWAP = psutil.swap_memory().total / 1024 / 1024
    Used_SWAP = (psutil.swap_memory().used / 1024 / 1024) * 100 / Total_SWAP
    mem_details = {"Total RAM [MB]": "%.2f" % Total_mem,
    "Used RAM [%]": "%.2f" % Used_mem,
    "Total SWAP [MB]": "%.2f" % Total_SWAP,
    "Used SWAP [%]": "%.2f" % Used_SWAP
    }
    
    if Used_mem >= 60:
        alarms += "Low memory : " + "%.2f" % Used_mem + "% of RAM used\n"
    if Used_SWAP >= 10:
        alarms += "Low memory : " + "%.2f" % Used_SWAP + "% of RAM used\n"
    
    for key, value in mem_details.items():
        format_output(key, value)

        
def get_partitions():
    """
    function that gets the usage of 
    all partitions in percentages.
    If a partition is more than 75%
    full, an alarm will be raised
    """
    global alarms
    print('Disk Partitions Usage')
    partitions_usage = {}
    for partition in psutil.disk_partitions():
        usage_percent = psutil.disk_usage(partition.mountpoint).percent
        partitions_usage[partition.mountpoint] = str(usage_percent) + '%'
        if usage_percent >= 75:
            alarms += 'The ' + partition.mountpoint + ' partition is ' + str(usage_percent) + '% full!\n'
        
    for key, value in partitions_usage.items():
        format_output(key, value)
    
    
#banner()
# Machine details
get_hardware_specs()
separate_sections()
# Network details
check_internet_connectivity()
get_ips()
separate_sections()
# OS related details
get_virtual_memory_SWAP()
separate_sections()
get_partitions()
separate_sections()

# if there are alarms, these will be displayed
if alarms != "":
    print('Active Alarms')
    print(alarms)

