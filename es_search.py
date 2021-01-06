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
import xlrd, xlwt
from xlutils.copy import copy as xl_copy
#from pyecharts import charts
#from pyecharts.charts import Line
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt





fan_body =   {
  "query": {
    "bool" : { 
      "must":{"range": {"Timestamp": {"gte": "now-5d"}}},
      "should":[
        {"range":{ "Fan0":{"gte": "4000"}}},
        {"range":{ "Fan0":{"lte": "3000"}}},
        {"range":{ "Fan1":{"gte": "4000"}}},
        {"range":{ "Fan1":{"lte": "3000"}}},
        {"range":{ "Fan2":{"gte": "4000"}}},
        {"range":{ "Fan2":{"lte": "3000"}}},
        {"range":{ "Fan3":{"gte": "4000"}}},
        {"range":{ "Fan3":{"lte": "3000"}}},
        {"range":{ "Fan4":{"gte": "4000"}}},
        {"range":{ "Fan4":{"lte": "3000"}}},
        {"range":{ "Fan5":{"gte": "4000"}}},
        {"range":{ "Fan5":{"lte": "3000"}}},
        {"range":{ "Fan6":{"gte": "4000"}}},
        {"range":{ "Fan6":{"lte": "3000"}}},
        {"range":{ "Fan7":{"gte": "4000"}}},
        {"range":{ "Fan7":{"lte": "3000"}}},
        {"range":{ "Fan8":{"gte": "4000"}}},
        {"range":{ "Fan8":{"lte": "3000"}}}
      ]
    }
  },
  "_source": ["Fan0","Fan1","Fan2","Fan3","Fan4","Fan5","Fan6","Fan7","Fan8","Location","Hostname","Timestamp"],
  "size": "10"
}

platform_body =   {
  "query": { 
    "bool": {
     "must":[
        {"range": {"Timestamp": {"gte": "now-5d"}}},
        {"match": { "State": "IOX XR RUN"}},
        {"match": { "Config_state": "PWR,NSHUT,MON"}}
        ]
    }
  },
  "_source": ["Node","Type","Plim","State","Config_state","Timestamp","Hostname","Platform_type"]
}

fpd_body = {
  "query":{
    "bool":{
      "must":{"range": {"Timestamp": {"gte": "now-5d"}}},
      "must_not":{"match":{"Upgrade":"Yes"}}
    }
  },
  "_source": ["Location","Cardtype","Version","Subtype","Currversion","Upgrade","Hostname","Timestamp"]
}

processes_memory_body = {
  "size": 10,
  "query":{
    "bool":{
      "must":{"range": {"Timestamp": {"gte": "now-5d"}}}
    }
  },
  "_source": ["Timestamp","Hostname","Node_id","Jid","Process","Text_kb","Data_kb","Stack_kb","Data_kb","Dynamic_kb"]
}

ntp_body = {
   "size": 10000,
   "sort": { "Timestamp": "desc"},
   "query": {
     "bool" : { 
      "must":{"range": {"Timestamp": {"gte": "now-15H"}}},
      "should":{"match": {"Command_name": "show ntp status"}}     
      }
      }
}

general_body = {
   "size": 10000,
   "sort": { "Timestamp": "desc"},
   "query": {
      "match_all": {}
   }
}

general_body_today = {
     "size": 10000,
     "sort": { "Timestamp": "desc"},
     "query": {
          "bool" : { 
               "must":{"range": {"Timestamp": {"gte": "now-4H"}}}
          }
     }
}


#es_address = "http://10.75.44.133:9200"
es_address = "http://127.0.0.1:9200"

#elastic = Elasticsearch(hosts= "10.75.44.133")
elastic = Elasticsearch(hosts= "127.0.0.1")
#index_database_1 = "hc9929_iox.platform_2020.09"
#index_database = "hc9929_iox.fans_2020.09"
#index_database_fpd = "hc9929_iox.fpd_2020.09"
#index_database_processes_memory = "hc.4837_iox.process.mem_2020.09"
index_database = ["cmi_vpn_a9k.ioxrvrf_2021.01"]

sheetname = ["vrf"]




list_fan_key = []


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

def search(sheetname,body,index_database,workbook):
     url = es_address  + "/"  + index_database
     res = requests.get(url)
     #print(res)
     list = []
     list_fan_key = []
     if res.status_code == 200:
          result= elastic.search(body=body,index=index_database)
          for key in result:
               if key == "hits":
                    dict = result[key]
                    for sub_key in dict:
                         if sub_key == "hits":
                              list = dict[sub_key]
                              #print(list)
                              for each_item in list:  #hit list
                                   #print(each_item)
                                   for each_item_key in each_item: 
                                        #print("all",each_item_key)
                                        if each_item_key == "_source": #get all fan 
                                             data_dict = each_item[each_item_key]
                                             for each_data_dict in data_dict:
                                                  list_fan_key.append(each_data_dict)
                                             #print(list_fan_key)
                                   break
                    break
     #print(list)
     write_excel(sheetname,list,list_fan_key,workbook)                             
                                   
def set_style(name,height,bold=False):
     style = xlwt.XFStyle()
     font = xlwt.Font()
     font.name = name
     font.bold = bold
     font.color_index = 4
     font.height = height
     style.font = font
     return style

def write_excel(sheetname,dict_list,list_fan_key,workbook):
     list = dict_list
     #create xls file
    
     rb = xlrd.open_workbook(workbook, formatting_info=True)
     wb = xl_copy(rb)
     sheet = wb.add_sheet(sheetname)
     row0 = list_fan_key
     for i in range(0,len(row0)):
          sheet.write(0,i,row0[i],set_style('Times New Roman',220,True))
     m = 1 #行号and order number
     for each_hits in list:
          for each_hits_sub in each_hits:
               if each_hits_sub == "_source":
                    for data in each_hits[each_hits_sub]:
                         for  n in range(len(row0)):
                              if data == row0[n]:
                                   sheet.write(m,n, each_hits[each_hits_sub][data],set_style('Times New Roman',220,True))  # 第一行第一列
          
          m = m + 1
     wb.save(workbook)

def paint():
     data = xlrd.open_workbook(r'all.xls')
     table = data.sheets()[1]
     
     x_data = []
     y_data = []
     y1_data = []
     for i in range(1,table.nrows):
          print("x",table.row_values(i)[5])
          print("y",table.row_values(i)[6])
          x_data.append(table.row_values(i)[6])
          y_data.append(table.row_values(i)[5])
          y1_data.append(table.row_values(i)[0])
     bar = charts.Bar()
     bar.add_xaxis(x_data)
     bar.add_yaxis("Data_kb",y1_data)
     bar.add_yaxis("Dynamic_kb",y_data)
     bar.render("show.html")
     
def paint_line():
     data = xlrd.open_workbook(r'all.xls')
     table = data.sheets()[1]
     
     x_data = []
     y_data = []
     y1_data = []
     for i in range(1,table.nrows):
          print("x",table.row_values(i)[5])
          print("y",table.row_values(i)[6])
          x_data.append(table.row_values(i)[7])
          y_data.append(table.row_values(i)[6])
          y1_data.append(table.row_values(i)[5])
     line = Line()
     line.add_xaxis(x_data)
     #line.add_yaxis("fib_mgr",y_data)
     line.add_yaxis("Fib_mgr_Dynamic_kb",y1_data)
     line.render("show_line.html")
     

if __name__ == "__main__":

     wb = xlwt.Workbook()
     sheet1 = wb.add_sheet('Sheet1')
     xls_filr_name_time = get_nowtime()[0]
     xls_file_name = "ncs_day2" + xls_filr_name_time + ".xls"
     wb.save(xls_file_name)
     workbook = xls_file_name

     for index in range(len(index_database)):
          print("len",len(index_database))
          print("index",index)
          print("sheetname",sheetname[index])
          print("index_database[index]",index_database[index])
          search(sheetname[index],general_body_today,index_database[index],workbook)


     
     #sheetname_fan = "fan"
     #sheetname_platform = "platform"
     #sheetname_fpd = "fpd"
     #sheetname_processes_memory = "processes_memory"
     #search(sheetname_fan,fan_body,index_database)
     #search(sheetname_platform,platform_body,index_database_1)
     #search(sheetname_fpd,fpd_body,index_database_fpd)
     #search(sheetname_processes_memory,processes_memory_body,index_database_processes_memory)
     #paint_line()