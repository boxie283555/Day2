import telnetlib
import time
import os
import re
import json
import sys
import datetime
import requests
import types
import threading
import logging
import textfsm
import fnmatch
import shutil
import logging.handlers
from elasticsearch import Elasticsearch
from multiprocessing import Manager, Process, Pool
import multiprocessing
import paramiko




current_dir = str(os.getcwd())+ "/"
parent_dir =  "hcdata_crs"
data_dir = current_dir + parent_dir
template_dir = current_dir + "crs/"
index_mapping_path = current_dir + "crs_index_mapping"


device_work_dir_list = list()
devices = list()
hostname = list()
ip = list()
username = list()
password = list()
os_type = list()
platform_mode = list()
login = list()
select_template = dict()

#xr_show_list = ["admin show environment fans","admin show platform","admin show hw-module fpd location all","admin show controllers fabric plane all", \
#"admin show controllers fabric connectivity all","admin show install active sum"]

os.path.join(template_dir)
os.environ["NET_TEXTFSM"] = template_dir

WAITE_FILE_TIME = 5
WAITE_COMMAND_TIME = 2




def get_nowtime():
     #获取当前时间
     time_now = int(time.time())
     #转换成localtime
     time_local = time.localtime(time_now)
     #转换成新的时间格式(2016-05-09 18:59:20)
     timestamp1 = time.strftime("%Y-%m-%d-%H-%M",time_local)
     timestamp2 = time.strftime("%Y.%m",time_local)
     timestamp3 = time.strftime("%H:%M:%S.%f %Z %a %b %d %Y",time_local)
     timestamp4 = time.strftime("%d",time_local)
     return timestamp1,timestamp2,timestamp3,timestamp4

def import_index_mapping(es_address,key_es):
     os.chdir(index_mapping_path)
     index_ext_time = get_nowtime()[1]
     host = set_eshost[key_es]
     elastic = Elasticsearch(hosts= host)
     for each_index in jsondir:
          index_database = jsondir[each_index] + index_ext_time
          url = es_address  + index_database
          res = requests.get(url)
          if res.status_code != 200:
               mapping_file = jsondir[each_index] + "mapping.json"
               with open(mapping_file, 'r', encoding='utf-8') as f:
                    data=json.loads(f.read())

               response = elastic.indices.create(index=index_database,body=data,ignore=400)
               if 'acknowledged' in response:
                    if response['acknowledged'] == True:
                         logger.info('import_index_mapping:{} INDEX MAPPING SUCCESS FOR INDEX'.format(response['index']))

               elif 'error' in response:
                    logger.info('import_index_mapping:ERROR {}'.format(response['error']['root_cause']))
                    logger.info('import_index_mapping:TYPE {}'.format(response['error']['type']))

               logger.info('import_index_mapping:response {}'.format(response))

def import_es_new(file_list,name):
     if len(file_list) == len(crs_command):
          logger.info('Import_es_new:{} there are {} Json file!'.format(name,len(file_list)))
     else:
          logger.warning('Import_es_new:{} there are {} Json file, but {} Json file is not exist!'.format(name,len(file_list),len(crs_command)-len(file_list)))

     index_database = ""
     for key_es in set_eshost:
          es_address = "http://" + str(set_eshost[key_es]) + ":9200/"

     os.chdir(data_dir)
     for key_compare in crs_command:
          key_diff = key_compare.replace(" ","_")
          key_diff_power = key_diff + "_old"
               
          for i in range(len(file_list)):
               file_split = os.path.splitext(file_list[i])
               file_head = str(file_split[0])
               start = file_head.find("%") + 1
               file_head_temp = file_head[start:]
               end = file_head_temp.find("%")
               key = file_head[start:start+end]
               if key.find(key_diff) == 0:
                    if key_diff_power == key:
                         #print("****************************************",key_diff_power)
                         index = str(jsondir[key])
                         index_date = get_nowtime()
                         index_database = index + index_date[1]
                         url = es_address + index_database + "/" + "_bulk" 
                         payload = open(file_list[i])
                         headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                         res = requests.post(url, data=payload, headers=headers)
                         if res.status_code == 200:
                              #print("The %s file import to ES OK!" % (file)) 
                              logger.info('Import_es_new:{}--{} import to ES OK!'.format(name,file_list[i]))
                         else:
                              #print("The %s file not import to ES!" % (file))
                              logger.warning('Import_es_new:{}--{} import to ES Failed!'.format(name,file_list[i]))
                         payload.close()
                         break
                    else:
                         index = str(jsondir[key])
                         index_date = get_nowtime()
                         index_database = index + index_date[1]
                         url = es_address + index_database + "/" + "_bulk" 
                         payload = open(file_list[i])
                         headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                         res = requests.post(url, data=payload, headers=headers)
                         if res.status_code == 200:
                              #print("The %s file import to ES OK!" % (file)) 
                              logger.info('Import_es_new:{}--{} import to ES OK!'.format(name,file_list[i]))
                         else:
                              #print("The %s file not import to ES!" % (file))
                              logger.warning('Import_es_new:{}--{} import to ES Failed!'.format(name,file_list[i]))
                         payload.close()
                         break
               else:
                    if i == len(file_list) - 1:
                         logger.warning('Import_es_new:{}--{} Json file is not exist!'.format(name,key_compare))

def timeconvert(name,showtime):
     if  "PRC" in str(showtime):
          showtime = showtime.replace("PRC", "CST")
     else:
          pass
     try:     
          showtime = datetime.datetime.strptime(showtime, '%H:%M:%S.%f %Z %a %b %d %Y')
     except ValueError:
          logger.warning('get_nowtime:{} - {} Please using the general zone setting'.format(name,showtime))
          #cust_time = get_nowtime()[2]
          #showtime = datetime.datetime.strptime(cust_time, '%H:%M:%S.%f %Z %a %b %d %Y')
     time1 = showtime.strftime('%Y-%m-%d')
     time2 = showtime.strftime('%H:%M:%S')
     time3 = time1 +"T"+time2+"+0800"
     return time3  

def modify_json(filename,name):
     os.chdir(data_dir)
     try:
        with open(filename,'r') as r:
            lines=r.readlines()
     except:
          logger.warning('modify_json:{}--{} json file does not exist.'.format(name,filename))
     
     with open(filename,'w') as w:
        if len(lines) == 1:
            new = '{"index":{}}'+'\n'
            new_line = str((lines[0])[1:-1])
            w.write(new)
            w.write(new_line)
            w.write("\n")  
        else:
            for row in lines:  
                if row.strip().startswith("["):   
                    new = '{"index":{}}'+'\n'
                    w.write(new)                   
                    continue
                elif row.strip().startswith("},"):    
                    new1 = '}'+'\n'+'{"index":{}}'+'\n'
                    w.write(new1)
                    continue
                elif row.strip().startswith("],"):  
                    raw = row.strip()
                    w.write(raw.strip('\n\t'))   
                    continue
                elif row.strip().startswith("]"):  
                    new3 = '\n'
                    w.write(new3)
                    continue
                else:
                    raw = row.strip()
                    w.write(raw.strip('\n\t'))   
            w.write("\n")  
     
def Get_data(filename):
    os.chdir(data_dir) 
    input_file = open(filename, encoding='utf-8')
    raw_text_data = input_file.read()
    input_file.close()
    return raw_text_data

def Get_templete(template_name):
    os.chdir(template_dir) 
    template = open(template_name)
    return template

def textfsm_result_conver_to_dic_new(fsm_header_list, fsm_content):
    result = list()
    for line in fsm_content:
        tmp_result_dic = dict(zip(fsm_header_list, line))
        result.append(tmp_result_dic)
    return result

def run(show_file, template_file):
    template = Get_templete(template_name= template_file)
    text_data = Get_data(filename=show_file)
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(text_data)
    res = textfsm_result_conver_to_dic_new(fsm_header_list= re_table.header, fsm_content=fsm_results)
    return res

def login_and_execcommand_crs(name,ip_address,user,passwd,platform,login_mode):
     login_flags = bool()
     #tn = telnetlib.Telnet()
     ssh = paramiko.SSHClient()
     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
     i = 0
     for i in range(3):
          try:
               ssh.connect(ip_address,port=22,username=user,password=passwd,timeout=5,allow_agent=False, look_for_keys=False)
          except:
               logger.critical('login_and_execcommand:{} connect error {} times'.format(name,i))
               login_flags = False
          channel = ssh.invoke_shell()
          resp = channel.recv(9999).decode('utf-8')
          if resp.rstrip().endswith("#"):
               logger.info('login_and_execcommand:{} connect success!!!!'.format(name))
               login_flags = True
               break
          else:
               logger.warning('login_and_execcommand:{} reconnecting....'.format(name))
               resp=""
               if i == 2:
                    logger.critical('login_and_execcommand:{} connect failed'.format(name))
                    login_flags = False

     if login_flags == True and platform == "CRS":
          dict3={} 
          file_list = []
          create_file_time = get_nowtime()
          os.chdir(data_dir)

          comm_ter_len = "ter len 0"
          channel.send(comm_ter_len + "\n")
          time.sleep(WAITE_COMMAND_TIME)

          #add clock
          command_clock = "show clock"
          dict_time = {}
          new_command_clock = command_clock.replace(" ","_")
          clock_txt_filename = name + "%" + new_command_clock + "%" + str(create_file_time[0]) + ".txt"
          f = open(str(clock_txt_filename),'w')
          channel.send(command_clock + "\n")
          time.sleep(WAITE_COMMAND_TIME)
          command_result_clock=""
          command_result_clock = channel.recv(9999).decode('utf-8')
          flags = True
          while  flags:
               if command_result_clock.rstrip().endswith("#"):
                    flags = False
               else:
                    time.sleep(WAITE_COMMAND_TIME)
                    command_result_clock += channel.recv(9999).decode('utf-8')
          f.write(command_result_clock)
          time.sleep(WAITE_FILE_TIME)
          f.close()
          time.sleep(WAITE_FILE_TIME)
          output_clock = run(show_file=clock_txt_filename, template_file=select_template[command_clock])
          for name_time in output_clock:
               for key in name_time:
                    showtime = str(name_time[key])
                    time_res = timeconvert(name,showtime)
                    name_time['Timestamp'] = time_res
                    dict_time = name_time

          #add hostname
          command_hostname = "show running hostname"
          new_command_hostname = command_hostname.replace(" ","_")
          hostname_txt_filename = name + "%" + new_command_hostname + "%" + str(create_file_time[0]) + ".txt"
          hostfile = open(hostname_txt_filename,'w')
          channel.send(command_hostname + "\n")
          time.sleep(WAITE_COMMAND_TIME)
          command_result_hostname=""
          command_result_hostname = channel.recv(9999).decode('utf-8')
          flags_host = True
          while  flags_host:
               if command_result_hostname.rstrip().endswith("#"):
                    flags_host = False
               else:
                    time.sleep(WAITE_COMMAND_TIME)
                    command_result_hostname += channel.recv(9999).decode('utf-8')
          hostfile.write(command_result_hostname)
          time.sleep(WAITE_FILE_TIME)
          hostfile.close()
          output_hostname = run(show_file=hostname_txt_filename, template_file=select_template[command_hostname])
          hostdict = {}
          for host_id in output_hostname:
               hostdict.update(host_id)  

          #add Platform type
          platform_type_dict = {"Platform_type":platform}

          #update all information to temp dict   
          dict3.update(dict_time)
          dict3.update(hostdict)
          dict3.update(platform_type_dict)

          
          for command_key in crs_command:
               cmddict = {"Command_name":command_key}
               dict3.update(cmddict)
               exec_command = command_key.replace(" ","_")
               command_txt_filename = name + "%" + exec_command + "%" + str(create_file_time[0]) + ".txt"
               command_file = open(command_txt_filename,'w')
               channel.send(crs_command[command_key] + '\n')
               time.sleep(WAITE_COMMAND_TIME)
               command_result = ""
               command_result = channel.recv(9999).decode('utf-8')
               flags_command = True
               while  flags_command:
                    if command_result.rstrip().endswith("#"):
                         flags_command = False
                    else:
                         time.sleep(WAITE_COMMAND_TIME)
                         command_result += channel.recv(9999).decode('utf-8')                     
               command_file.write(command_result)
               time.sleep(WAITE_FILE_TIME)
               command_file.close()
               if command_key == "admin show environment power-supply":
                    try:
                         output_command = run(show_file=command_txt_filename, template_file=select_template[command_key])
                         if len(output_command) == 0:
                              try:
                                   output_command = run(show_file=command_txt_filename, template_file="CRS_OLD_cisco_xr_admin_show_environment_power_supply.textfsm")
                                   if len(output_command) == 0:
                                        logger.warning('login_and_execcommand: {}_{} exec ok but no record match the template. the json can not create!!!!'.format(name,crs_command[command_key]))
                                        continue
                                   else:
                                        #output json file
                                        for command_dict in output_command:
                                             command_dict.update(dict3)  
                                        json_filename = name + "%" + exec_command + "_old%" + str(create_file_time[0]) + ".json"
                                        command_json_file = open(json_filename,'w')
                                        json_data_command = json.dumps(output_command, indent=1)
                                        time.sleep(WAITE_FILE_TIME)
                                        command_json_file.write(json_data_command)
                                        time.sleep(WAITE_FILE_TIME)
                                        #print ("%s %s exec ok and write completed." % (name,command))
                                        logger.info('login_and_execcommand: {}-{}old exec ok and write completed!'.format(name,crs_command[command_key]))

                                        command_json_file.close()
                                        file_list.append(json_filename)
                                        modify_json(json_filename,name)
                              except:
                                   logger.warning('login_and_execcommand: {}-{} template error!'.format(command_txt_filename,select_template[command_key]))
                         else:
                              #output json file
                              for command_dict in output_command:
                                   command_dict.update(dict3)  
                              json_filename = name + "%" + exec_command + "%" + str(create_file_time[0]) + ".json"
                              command_json_file = open(json_filename,'w')
                              json_data_command = json.dumps(output_command, indent=1)
                              time.sleep(WAITE_FILE_TIME)
                              command_json_file.write(json_data_command)
                              time.sleep(WAITE_FILE_TIME)
                              #print ("%s %s exec ok and write completed." % (name,command))
                              logger.info('login_and_execcommand: {}-{} exec ok and write completed!'.format(name,crs_command[command_key]))

                              command_json_file.close()
                              file_list.append(json_filename)
                              modify_json(json_filename,name)
                    except:
                         logger.warning('login_and_execcommand: {}-{} template error!'.format(command_txt_filename,select_template[command_key]))
               else:
                    try:
                         output_command = run(show_file=command_txt_filename, template_file=select_template[command_key])
                    except:
                         logger.warning('login_and_execcommand: {}-{} template error!'.format(command_txt_filename,select_template[command_key]))
                    if len(output_command) == 0:
                         logger.warning('login_and_execcommand: {}_{} exec ok but no record match the template. the json can not create!!!!'.format(name,crs_command[command_key]))
                         continue  
                    else:             
                         for command_dict in output_command:
                              command_dict.update(dict3)
                    #output json file
                    json_filename = name + "%" + exec_command + "%" + str(create_file_time[0]) + ".json"
                    command_json_file = open(json_filename,'w')
                    json_data_command = json.dumps(output_command, indent=1)
                    time.sleep(WAITE_FILE_TIME)
                    command_json_file.write(json_data_command)
                    time.sleep(WAITE_FILE_TIME)
                    #print ("%s %s exec ok and write completed." % (name,command))
                    logger.info('login_and_execcommand: {}-{} exec ok and write completed!'.format(name,crs_command[command_key]))
                    command_json_file.close()
                    file_list.append(json_filename)
                    modify_json(json_filename,name)
          try:
               channel.send("admin clear controller fabric statistics plane all" + "\n")
               time.sleep(WAITE_FILE_TIME)
               channel.send("\n")
               time.sleep(WAITE_FILE_TIME)
          except:
               logger.critical('login_and_execcommand:{} error'.format("clear counters"))     
          channel.send("exit" + "\n")
          #import_es_new(file_list,name)

def mv_files():
     #raw_directory_list = ["show_running_hostname","show_clock","admin show environment fan","admin show platform","admin show hw-module fpd location all","admin show controllers fabric plane all", \
     #"admin show controllers fabric connectivity all","admin show install active sum"]
     command_new_list = []
     dir_list = []
     os.chdir(data_dir)
     for command_key in crs_command:
          command_new = command_key.replace(" ","_")
          command_new_list.append(command_new)
          try:
               os.mkdir(command_new)
          except:
               #print("directory is exists!!!")
               logger.info('mv_files: {} directory is exists!!!'.format(command_new))
     try:
          clock_dir = "show_clock"
          os.mkdir(clock_dir)
     except:
          #print("directory is exists!!!")
          logger.info('mv_files: {} directory is exists!!!'.format(clock_dir))
     try:
          hostname_dir = "show_running_hostname"
          os.mkdir(hostname_dir)
     except:
          #print("directory is exists!!!")
          logger.info('mv_files: {} directory is exists!!!'.format(hostname_dir))
     try:
          power_dir = "admin_show_environment_power-supply_old"
          os.mkdir(power_dir)
     except:
          #print("directory is exists!!!")
          logger.info('mv_files: {} directory is exists!!!'.format(power_dir))
     
     command_new_list.append(clock_dir)
     command_new_list.append(hostname_dir)
     command_new_list.append(power_dir)


     dir_list = command_new_list
     dir_dict = dict(zip(command_new_list, dir_list))

     for f_name in os.listdir(data_dir):
          for key in dir_dict:
               pattern = "*" + dir_dict[key] + "%" + "*"
               if fnmatch.fnmatch(f_name, pattern):
                    temp_dir = data_dir + "/" + dir_dict[key]
                    shutil.move(f_name,temp_dir)
     logger.info('mv_files: all files moved success')
 

os.chdir(current_dir)

startTime = datetime.datetime.now()
logfile_time = get_nowtime()

logfilename_warn = data_dir + "/log/" + "Day2check_warning_" + logfile_time[0] + ".log"
logfilename_info = data_dir + "/log/" + "Day2check_info_" + logfile_time[0] + ".log"
logger = logging.getLogger("logger")

handler_term = logging.StreamHandler()
handler_warn = logging.FileHandler(filename=logfilename_warn)
handler_info = logging.FileHandler(filename=logfilename_info)

logger.setLevel(logging.DEBUG)
handler_term.setLevel(logging.DEBUG)
handler_info.setLevel(logging.INFO)
handler_warn.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
handler_term.setFormatter(formatter)
handler_info.setFormatter(formatter)
handler_warn.setFormatter(formatter)

logger.addHandler(handler_term)
logger.addHandler(handler_info)
logger.addHandler(handler_warn)

with open('template_v1.conf') as f:
     select_template = dict(x.strip().strip("\n\t").split("::", 1) for x in f)
with open('es_file_v1.conf') as esf:
     jsondir = dict(x.strip().strip("\n\t").split("::", 1) for x in esf)
with open('hc_check_env.conf') as envf:
     set_eshost = dict(x.strip().strip("\n\t").split("::", 1) for x in envf)
with open('command_alias_matrix_v1.conf') as command_alias:
     crs_command = dict(x.strip().strip("\n\t").split("::", 1) for x in command_alias)


with open ('device.crs.txt') as devices_file:
     for device_node in devices_file:
          devices = re.split("::",device_node)
          hostname.append(devices[0].strip())
          ip.append(devices[1].strip())
          username.append(devices[2].strip())
          password.append(devices[3].strip())
          os_type.append(devices[4].strip())
          platform_mode.append(devices[5].strip())
          login.append(devices[6].strip())

try:
     os.mkdir(parent_dir)
except FileExistsError:
     #print("%s Device Directory is Exist,So using the raw directory" % (parent_dir))
     logger.info('_main_: {} Device Directory is Exist,So using the raw directory!'.format(parent_dir))


  
if __name__ == '__main__':
     logger.info('_main_: start time:{}!'.format(startTime))
     today = get_nowtime()[3]
     if today == "1" or today == "01":
          for key_es in set_eshost:
               es_address = "http://" + str(set_eshost[key_es]) + ":9200/"
               import_index_mapping(es_address,key_es)

     cpus = multiprocessing.cpu_count()
     p = multiprocessing.Pool(cpus*1)
     for name,ip_address,user,passwd,platform,login_mode in zip(hostname,ip,username,password,platform_mode,login):
          result =p.apply_async(login_and_execcommand_crs, args=(name,ip_address,user,passwd,platform,login_mode,))
     logger.info("Waiting for all subprocesses done...")
     p.close()
     p.join()
     logger.info('_main_: Total execution time:{}!'.format(datetime.datetime.now() - startTime))
     mv_files()






     
