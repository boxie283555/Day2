#!/usr/bin/env python3
# coding: utf-8

#Day2 log search tools Jing 2020.04 V1.0

from common import write_log, latest_filename, filename_time, valid_ip, check_tcp
from time import strftime, localtime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import Transport
from elasticsearch.connection import RequestsHttpConnection
import json
import sys
import conf
from tqdm import tqdm
import pandas as pd
import re
import time
import argparse
from retrying import retry
import datetime
from dateutil.parser import parse
import operator

class eshc:
    def __init__(self):
        "aaa"

    def has_conf(self, es_ip, es_port):
        """
        es ip and port is correct ?
        :return:
        """

        if not valid_ip(es_ip):
            write_log("ES ip address error", "purple_red")
            write_log("ES ip address error", log_name=self.log_error_name, no_print=True)
            self.error_tag = True
            exit(1)
            return False

        if not check_tcp(es_ip, es_port):
            write_log("ES {} port {} is unreachable".format(es_ip, es_port), "purple_red")
            write_log("ES {} port {} is unreachable".format(es_ip, es_port), log_name=self.log_error_name, no_print=True)
            self.error_tag = True
            exit(1)
            return False
        else:
            write_log("ES {} port {} is open".format(es_ip, es_port), "green")

        return True

    def open_rules_json (self,dir,filename):
        '''
        :打开目录中check json文件
        '''
        # syslog_json_path = input("请输入syslog json文件名：")
        rules_json_path = sys.path[0] + dir + filename
        try:
            with open(rules_json_path, 'r') as load_f:
                self.rules_json_load_dict = json.load(load_f)
            write_log("explain file \"{}\" load success".format(rules_json_path), "blue")
        except Exception as e:
            write_log("explain file \"{}\" load failed".format(rules_json_path), "purple_red")
            write_log("error message \"{}\" ".format(e), "red")
            write_log("explain file \"{}\" load failed".format(rules_json_path), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            exit(1)

    def open_json_dict (self,dir,filename):
        '''
        :打开目录中check json文件
        '''
        # syslog_json_path = input("请输入syslog json文件名：")
        json_path = sys.path[0] + dir + filename
        try:
            with open(json_path, 'r') as load_f:
                json_load_dict = json.load(load_f)
            return json_load_dict
            write_log("explain file \"{}\" load success".format(json_path), "blue")
        except Exception as e:
            write_log("explain file \"{}\" load failed".format(json_path), "purple_red")
            write_log("error message \"{}\" ".format(e), "red")
            write_log("explain file \"{}\" load failed".format(json_path), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            exit(1)

    def el2json(self, dir, filename, es_ip, es_port, es_search_type, es_scroll, es_size, es_timeout, es_index):

        # 打开查询json文件，在ES中进行搜索，并将结果保存到数组
        query_json_path = sys.path[0] + dir + filename
        es_query_result = []
        try:
            with open(query_json_path, 'r') as load_f:  # 打开json文件
                query_json_to_dict = json.load(load_f)
            write_log("query json file \"{}\" load succeed".format(query_json_path), "blue")
        except Exception as e:
            write_log("query json file \"{}\" load failed".format(query_json_path), "purple_red")
            write_log("error message \"{}\" ".format(e), "red")
            write_log("query json file \"{}\" load failed".format(query_json_path), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            self.index_open_success = False
            return es_index, es_query_result
        try:
            es = Elasticsearch([es_ip], port=es_port, timeout=es_timeout)
        except Exception as e:
            write_log("ES {} port {} connected failed ".format(es_ip, es_port), "purple_red")
            write_log("error message \"{}\" ".format(e), "red")
            write_log("ES {} port {} connected failed ".format(es_ip, es_port), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            exit(1)
        index_type = eval('conf.INDEX_TYPE_' + self.customer)  # 索引类型

        if es.indices.exists(es_index) == False:
            write_log("elasticsearch index \"{}\" not exist".format(es_index), "purple_red")
            self.index_open_success = False
            write_log("elasticsearch index \"{}\" not exist".format(es_index), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            return es_index, es_query_result
        else:
            write_log("elasticsearch index \"{}\" exist , query starting".format(es_index), "blue")

        try:
            result_iterator = helpers.scan(client=es, query=query_json_to_dict, index=es_index, doc_type=index_type,
                                           scroll=es_scroll, size=es_size, request_timeout=es_timeout,
                                           preserve_order=False)
            count = 0
            es_query_result = []
            for _result_iterator in tqdm(result_iterator):
                es_query_result.append(_result_iterator)
                count += 1
            write_log("elasticsearch index \"{}\" search was successful, a total of {} records were found".format(es_index,count),"bluish_blue")
        except Exception as e:
            write_log("elasticsearch index \"{}\" search failed".format(es_index), "purple_red")
            write_log("error message \"{}\"".format(e), "red")
            self.index_open_success = False
            write_log("elasticsearch index \"{}\" search failed".format(es_index), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            return es_index, es_query_result
        if es_query_result == []:
            self.error_tag = True
            write_log(
                "got es index \"{}\" data is empty".format(
                    self.current_index),
                "red")
            write_log(
                "got es index \"{}\" data is empty".format(
                    self.current_index),
                log_name=self.log_error_name, no_print=True)
        return es_index, es_query_result


    #从check_json中获得es结果每个_source的检查条件
    def get_check_list(self,check_list,es_query_result_source):
        try:
            ops_set = {"=", "!=", ">", ">=", '<', "<="}
            ops_dict = {'=': operator.eq, "!=": operator.ne, ">": operator.gt, ">=": operator.ge, '<': operator.lt,
                        '<=': operator.le}
            conditions_counter = len(self.rules_json_load_dict[check_list].keys()) - 1
            class_result = False
            sub_class_result = False
            count = 1
            each_class_value_list= [0]*6
            while count <= conditions_counter:
                conditions_num = 'conditions_' + str(count)
                # 得到条件列表
                class_list = self.rules_json_load_dict[check_list][conditions_num]['class']
                if class_list==[]:
                    check_items = self.rules_json_load_dict[check_list][conditions_num]['check']
                    # print(check_items)
                    return check_items
                # 所有条件数组循环，条件组之间为与的关系，<class 'list'>: [{'location': ['fullmatch', 'Upper', '$']}]
                for each_class_dict in class_list:
                    # 子条件组列表循环，包含子条件 <class 'dict'>: {'location': ['fullmatch', 'Upper', '$']}
                    for key in each_class_dict:
                        each_class_key = key
                        each_class_values_list = each_class_dict[key]
                        # 子条件中的列表值循环，<class 'dict'>: {'location': ['fullmatch', 'Upper', '$']}
                        class_count = 1
                        for each_class_value in each_class_values_list:
                            if each_class_value not in self.delimiter:
                                each_class_value_list[class_count] = each_class_value
                                class_count += 1
                                continue

                            if each_class_value_list[1] in ops_set:
                                es_source_data = self.get_num_from_str(str(es_query_result_source[each_class_key]))
                                if es_source_data is None:
                                    write_log(
                                        "index \"{}\" check list ope_set process number transform failed , host \"{}\"  number data is {} ".format(
                                            self.current_index, es_query_result_source[self.log_error_tag],
                                            es_query_result_source[each_class_key]), "purple_red")
                                    write_log(
                                        "index \"{}\" check list ope_set process number transform failed , host \"{}\"  number data is {} ".format(
                                            self.current_index, es_query_result_source[self.log_error_tag],
                                            es_query_result_source[each_class_key]),
                                        log_name=self.log_error_name, no_print=True)
                                    self.error_tag = True
                                    sub_class_result = False
                                    break
                                if ops_dict[each_class_value_list[1]](float(es_source_data),float(each_class_value_list[2])):
                                    sub_class_result = True
                                else:
                                    sub_class_result = False
                                    break
                            else:
                                re_method ='re.'+ each_class_value_list[1]
                                class_match = eval(re_method)(each_class_value_list[3], es_query_result_source[each_class_key])

                                if each_class_value_list[2] != 'not':
                                    if class_match is not None:
                                        sub_class_result = True
                                    else:
                                        sub_class_result = False
                                        break
                                else:
                                    if class_match is None:
                                        sub_class_result = True
                                    else:
                                        sub_class_result = False
                                        break

                        if sub_class_result is True:
                            class_result = True
                        else:
                            class_result = False
                            break
                    if class_result is True:
                        break
                if class_result is True:
                    check_items = self.rules_json_load_dict[check_list][conditions_num]['check']
                    #print(check_items)
                    return check_items
                count+=1
        except Exception as e:
            write_log("get check list failed", "purple_red")
            write_log("error message \"{}\"".format(e), "red")
            write_log("index \"{}\" data get check list failed".format(self.current_index), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            check_items = []
            return check_items

    def check_result(self,check_list,check_items,es_query_result_source):
        try:
            headers = self.rules_json_load_dict[check_list]['header']
            result_list = []
            result_level_list = []
            final_result_list = []
            final_result_level_list = []
            check_key_not_match_es_key_value = ''
            each_check_item_value_list = [0]*6
            check_key_match_es_key = False
            ops_set = {"=","!=",">",">=",'<',"<="}
            ops_dict = {'=': operator.eq, "!=": operator.ne, ">": operator.gt, ">=": operator.ge, '<': operator.lt,'<=': operator.le}  # etc
            #分解check内容，<class 'list'>: [{'fan\\d+': ['3500|>', '4500|<'], 'hostname': ['CRS16|search']}, {'hostname': ['CRS16|search']}]
            #逻辑或
            for each_check_item in check_items:

                # 分解check单项内容<class 'list'>: [{'fan\\d+': ['>', '4000', 'and', '<', '5000', '$']}, {'fan\\d': ['<', '2000', '$']}]
                #逻辑与
                for each_check_item_key in each_check_item:
                    check_result = False
                    for each_header in headers:
                        check_header_match_result = re.fullmatch(each_check_item_key, each_header)
                        if check_header_match_result is None:
                            continue
                        if each_header not in es_query_result_source.keys():
                            check_key_match_es_key = False
                            check_key_not_match_es_key_value = each_header
                            continue
                        check_key_match_es_key = True
                        #分解check单项<class 'dict'>: {'fan\\d+': ['>', '4000', '1',and', '<', '5000','2','$']}
                        rule_count = 1
                        for each_check_item_value in each_check_item[each_check_item_key]:
                            rule_count_mod_number = rule_count % 6
                            each_check_item_value_list[rule_count_mod_number] = each_check_item_value
                            if each_check_item_value not in self.delimiter:
                                rule_count+=1
                                continue
                            #重置列表位置计数器
                            rule_count = 1
                            sub_check_result = False
                            if each_check_item_value_list[1] in ops_set:
                                es_source_data = self.get_num_from_str(str(es_query_result_source[each_header]))
                                if es_source_data is None:
                                    #write_log(
                                    #    "index \"{}\" ope_set process number transform failed , host \"{}\"  number data is {} ".format(
                                    #        self.current_index,es_query_result_source[self.log_error_tag],es_query_result_source[each_header]), "purple_red")
                                    #write_log(
                                    #    "index \"{}\" ope_set process number transform failed , host \"{}\"  number data is {} ".format(
                                    #        self.current_index,es_query_result_source[self.log_error_tag],es_query_result_source[each_header]),
                                    #    log_name=self.log_error_name, no_print=True)
                                    #self.error_tag = True
                                    sub_check_result = False
                                    break
                                if ops_dict[each_check_item_value_list[1]](float(es_source_data),float(each_check_item_value_list[2])):
                                    sub_check_result_level = each_check_item_value_list[3]
                                    sub_check_result = True
                                else:
                                    sub_check_result = False
                                    break
                            elif each_check_item_value_list[1] == "copstr":
                                try:
                                    es_source_data_source = str(es_query_result_source[each_header])
                                    es_source_data_dest = str(es_query_result_source[each_check_item_value_list[2]])
                                except Exception as e:
                                    write_log(
                                        "index \"{}\" copeqstr process number transform failed , host \"{}\" source is {} dest is {} ".format(
                                            self.current_index,es_query_result_source[self.log_error_tag], es_query_result_source[each_header],
                                            es_query_result_source[each_check_item_value_list[2]]), "purple_red")
                                    write_log(
                                        "index \"{}\" copeqstr process number transform failed , host \"{}\" source is {} dest is {} ".format(
                                            self.current_index,es_query_result_source[self.log_error_tag], es_query_result_source[each_header],
                                            es_query_result_source[each_check_item_value_list[2]]),
                                        log_name=self.log_error_name, no_print=True)
                                    self.error_tag = True
                                    sub_check_result = False
                                    break
                                if ops_dict[each_check_item_value_list[3]](es_source_data_source,es_source_data_dest):
                                    sub_check_result = True
                                    sub_check_result_level = each_check_item_value_list[4]
                                else:
                                    sub_check_result = False
                                    break
                            elif each_check_item_value_list[1] == "divnum":
                                es_source_data_dividend = self.get_num_from_str(str(es_query_result_source[each_header]))
                                es_source_data_divisor = self.get_num_from_str(str(es_query_result_source[each_check_item_value_list[2]]))
                                #转换失败则判断为不符合条件,写错误log
                                if es_source_data_dividend is None or es_source_data_divisor is None:
                                    write_log(
                                        "index \"{}\" divltnum process number transform failed , host \"{}\" dividend is {} subtrahend is {} ".format(
                                            self.current_index,es_query_result_source[self.log_error_tag], es_query_result_source[each_header],
                                            es_query_result_source[each_check_item_value_list[2]]), "purple_red")
                                    write_log(
                                        "index \"{}\" divltnum process number transform failed , host \"{}\" dividend is {} subtrahend is {} ".format(
                                            self.current_index, es_query_result_source[self.log_error_tag],es_query_result_source[each_header],
                                            es_query_result_source[each_check_item_value_list[2]]),
                                        log_name=self.log_error_name, no_print=True)
                                    self.error_tag = True
                                    sub_check_result = False
                                    break
                                div_value = float(es_source_data_dividend) / float(es_source_data_divisor)
                                if ops_dict[each_check_item_value_list[3]](div_value, float(each_check_item_value_list[4])):
                                    sub_check_result = True
                                    sub_check_result_level = each_check_item_value_list[5]
                                else:
                                    sub_check_result = False
                                    break
                            elif each_check_item_value_list[1] == "subdate":
                                es_source_data_minuend = self.str_to_date(es_query_result_source[each_header])
                                es_source_data_subtrahend = self.str_to_date(es_query_result_source[each_check_item_value_list[2]])
                                if es_source_data_minuend is not None and es_source_data_subtrahend is not None:
                                    sub_value = abs((es_source_data_minuend - es_source_data_subtrahend).days)
                                    if ops_dict[each_check_item_value_list[3]](sub_value,int(each_check_item_value_list[4])):
                                        sub_check_result = True
                                        sub_check_result_level = each_check_item_value_list[5]
                                    else:
                                        sub_check_result = False
                                        break
                                else:
                                    write_log("index \"{}\" date transform failed ,host \"{}\" minuend is {} subtrahend is {} ".format(self.current_index,es_query_result_source[self.log_error_tag],es_source_data_minuend, es_source_data_subtrahend), "purple_red")
                                    write_log("index \"{}\" date transform failed ,host \"{}\" minuend is {} subtrahend is {} ".format(self.current_index,es_query_result_source[self.log_error_tag],es_source_data_minuend, es_source_data_subtrahend),log_name=self.log_error_name, no_print=True)
                                    sub_check_result = False
                                    self.error_tag = True
                                    break
                            else:
                                re_method = 're.' + each_check_item_value_list[1]
                                re_result = eval(re_method)(each_check_item_value_list[3],str(es_query_result_source[each_header]))
                                if each_check_item_value_list[2] != 'not':
                                    if re_result is not None:
                                        sub_check_result = True
                                        sub_check_result_level = each_check_item_value_list[4]
                                    else:
                                        sub_check_result = False
                                        break
                                else:
                                    if re_result is None:
                                        sub_check_result = True
                                        sub_check_result_level = each_check_item_value_list[4]
                                    else:
                                        sub_check_result = False
                                        break

                        if sub_check_result is True:
                            check_result = True
                            result_list.append(self.excel_col_num_to_name(headers.index(each_header)+1))
                            result_level_list.append(sub_check_result_level)
                            #result_list.append(es_query_result_source[each_header])
                            #print (each_header)
                            #print (es_query_result_source[each_header])
                     #与条件中某条不为真，则跳出与条件循环
                    if check_result is not True:
                        result_list = []
                        result_level_list = []
                        break
                if check_key_match_es_key is not True:
                    self.error_tag = True
                    write_log("index \"{}\" host \"{}\" check item {} not match es data key or rules json check item not match check header".format(self.current_index,es_query_result_source[self.log_error_tag],check_key_not_match_es_key_value), "red")
                    write_log("index \"{}\" host \"{}\" check item {} not match es data key or rules json check item not match check header".format(self.current_index,es_query_result_source[self.log_error_tag],check_key_not_match_es_key_value),log_name=self.log_error_name, no_print=True)

                if check_result is not True:
                    result_list = []
                    result_level_list = []
                if result_list != []:
                    final_result_list.extend(result_list)
                    final_result_level_list.extend(result_level_list)

            return final_result_list,final_result_level_list
        except Exception as e:
            write_log("\"{}\" index host \"{}\" checklist failed".format(self.current_index,es_query_result_source[self.log_error_tag]), "purple_red")
            write_log("error message \"{}\"".format(e), "red")
            write_log("\"{}\" index host \"{}\" data check result failed".format(self.current_index,es_query_result_source[self.log_error_tag]), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            final_result_list = []
            final_result_level_list =[]
            return final_result_list,final_result_level_list

    def dict2dataframe(self, hits_hits,check_list,sort_col):
        check_result_df = pd.DataFrame()
        check_highlight_list = []
        check_level_list = []
        if check_list == []:
            return check_result_df,check_highlight_list,check_level_list
        try:
            header_list = self.rules_json_load_dict[check_list]['header']
        except Exception as e:
            write_log("\"{}\" index rules json get \"{}\" checklist failed".format(self.current_index,check_list), "purple_red")
            write_log("error message \"{}\"".format(e), "red")
            write_log("\"{}\" index rules json get \"{}\" checklist failed".format(self.current_index,check_list), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            return check_result_df, check_highlight_list, check_level_list

        # 将搜索后的结果json 存入原始DF
        df_list =[]
        df_list_dict = {}
        header_dict = {}
        #转换表头为字典格式，用来进行DF表头更改
        header_count = 0
        for each_header in header_list:
            header_dict[header_count] = str(each_header)
            header_count+=1
        #print (header_dict)


        #条件判断数量
        conditions_counter = len(self.rules_json_load_dict[check_list].keys())-1
        result_list=[]
        high_light_list = []
        self.count_match = 2
        self.count_body = 1
        write_log("health check data begins to be imported into the DF original table".format(), "green")
        for _hits in tqdm(hits_hits):
            df_list=[]
            _source= _hits['_source']
            #print (_source)
            check_items = self.get_check_list(check_list=check_list,es_query_result_source=_source)
            result_list,result_level_list = self.check_result(check_list = check_list, check_items = check_items, es_query_result_source = _source)
            #提取查询到符合rule json的数据
            if result_list!=[]:
                #生成check sheet high light 坐标
                #check_highlight_list.extend(self.high_light_list(result_list,self.count_match+self.check_sheet_first_line-1))
                #check_level_list.extend(result_level_list)
                #取出es中匹配的数据
                for header in header_list:
                    if header in _source.keys():
                        df_list.append(_source[header])
                    else:
                        self.error_tag = True
                        df_list.append('NULL')
                        write_log("index \"{}\" host \"{}\" rules header \"{}\" not match es data key".format(self.current_index,_source[self.log_error_tag],header), "red")
                        write_log("index \"{}\" host \"{}\" rules header \"{}\" not match es data key".format(self.current_index,_source[self.log_error_tag],header,),log_name=self.log_error_name, no_print=True)
                #提取后的数据组合成dict 准备放到df里
                df_list.append(result_list)
                df_list.append(result_level_list)
                df_list_dict[self.count_match-1] = df_list
                self.count_match+=1
            self.count_body += 1

        #DF 排序和生成execl坐标
        if df_list_dict != {}:
            check_result_df = check_result_df.from_dict(df_list_dict, orient='index')
            check_result_df.rename(columns=header_dict, inplace=True)
            check_result_df = check_result_df.sort_values(by=sort_col)
            check_result_df.reset_index(drop=True, inplace=True)
            high_light_set_count = 2 #与self.count_match起始值一致
            col_wide = check_result_df.shape[1]
            # 从df中提取high_light位置，组合成excel表格坐标，提取告警级别
            for tup in zip(check_result_df[check_result_df.columns[col_wide - 2]],check_result_df[check_result_df.columns[col_wide - 1]]):
                for each_high_light in tup[0]:
                    check_highlight_list.extend(self.high_light_list(each_high_light,high_light_set_count+self.check_sheet_first_line-1))
                check_level_list.extend(tup[1])
                high_light_set_count+=1
            #删除DFexcle 坐标列
            check_result_df.drop([check_result_df.columns[col_wide - 1]], axis=1, inplace=True)
            check_result_df.drop([check_result_df.columns[col_wide - 2]], axis=1, inplace=True)

        write_log("The data is imported into the DF original table, and a total of {} records are imported".format(self.count_match - 2), "yellow")
        return check_result_df,check_highlight_list,check_level_list

    def df2xlsx(self, check_result_df,check_list, high_light,level_list,fg_color,font_color):
        # 保存聚合DF、和排序的原始DF 到excel两个表单
        check_result_df_sheet_row = check_result_df.shape[0]
        check_result_df_sheet_col = check_result_df.shape[1]
        write_log("DF table write to excel start".format(self.count_body), "green")
        check_result_df.to_excel(self.writer, sheet_name='all', startrow=self.checkall_counter, header=0, encoding='utf-8',index=False)
        check_result_df.to_excel(self.writer, sheet_name=check_list, startrow=self.check_sheet_first_line, header=0, encoding='utf-8',index=False)
        # 表头处理
        workbook = self.writer.book
        worksheet = self.writer.sheets[check_list]
        worksheet_all = self.writer.sheets['all']
        if self.index_count % 2 == 0:
            head_color = workbook.add_format({'fg_color': '#FFEE99', 'font_color': 'blue', 'bold': True})
            #all sheet 超链接 军校蓝 深紫色
            hyperlink_check_top_color = workbook.add_format({'fg_color': '#5F9EA0', 'font_color': 'yellow', 'bold': True})
            hyperlink_local_check_color = workbook.add_format({'fg_color': '#D2691E', 'font_color': 'white', 'bold': True})

        else:
            head_color = workbook.add_format({'fg_color': '#2dB054', 'font_color': 'white', 'bold': True})
            #all sheet 超链接 午夜蓝色 幽灵白色
            hyperlink_check_top_color = workbook.add_format({'fg_color': '#191970', 'font_color': '#F8F8FF', 'bold': True})
            hyperlink_local_check_color = workbook.add_format({'fg_color': '#ddf3ff', 'font_color': 'black', 'bold': True})

        hyperlink_all_top_color = workbook.add_format({'fg_color': '#00008B', 'font_color': '#FFFF00', 'bold': True})
        hyperlink_all_check_color = workbook.add_format({'fg_color': '#9932CC', 'font_color': 'white', 'bold': True})


        # bg is PaleVioletRed ,font is Gold
        high_light_color = workbook.add_format({'bg_color': fg_color, 'font_color': font_color,'bold': True})
        count = 0
        # write check sheet easy go to link
        worksheet.write_url('A1', 'internal:all!A1')
        worksheet.write("A1", "back all top", hyperlink_all_top_color)
        worksheet.write_url('B1', 'internal:all!A' + str(self.checkall_counter-1))
        worksheet.write("B1", "back all " + check_list, hyperlink_all_check_color)

        worksheet.write_url('A' + str(check_result_df_sheet_row + self.check_sheet_first_line + 2), 'internal:all!A1')
        worksheet.write("A" + str(check_result_df_sheet_row + self.check_sheet_first_line + 2), "back all top", hyperlink_all_top_color)
        worksheet.write_url('B' + str(check_result_df_sheet_row + self.check_sheet_first_line + 2), 'internal:all!A' + str(self.checkall_counter - 1))
        worksheet.write("B" + str(check_result_df_sheet_row + self.check_sheet_first_line + 2), "back all " + check_list, hyperlink_all_check_color)

        #all sheet 分表定位符
        worksheet_all.write_url("A"+str(self.checkall_counter-1), 'internal:all!A1')
        worksheet_all.write("A"+str(self.checkall_counter-1), check_list, high_light_color)

        # write all sheet easy go to check link
        check_index_cell_mod = self.index_with_data_count % eval('conf.CHECKALL_SHEET_HYPERLINK_' + self.customer) + 1
        check_index_cell_quotient = self.index_with_data_count // eval('conf.CHECKALL_SHEET_HYPERLINK_' + self.customer) + 1
        #在all sheet 开头两行放置分sheet 超链接，目前支持最大48个
        check_index_cell_coordinate = self.excel_col_num_to_name(check_index_cell_mod)+str(check_index_cell_quotient)
        #all sheet 超链接到各个check sheet
        worksheet_all.write_url(check_index_cell_coordinate, 'internal:'+ check_list +'!A1')
        worksheet_all.write(check_index_cell_coordinate, check_list + ' sheet', hyperlink_check_top_color)

        # write all sheet easy go to all local link
        local_check_index_cell_mod = self.index_with_data_count % eval('conf.CHECKALL_SHEET_HYPERLINK_' + self.customer) + 1
        local_check_index_cell_quotient = self.index_with_data_count // eval('conf.CHECKALL_SHEET_HYPERLINK_' + self.customer) + eval('conf.CHECKALL_SHEET_LOCAL_HYPERLINK_FIRST_ROW_' + self.customer)
        # 在all sheet 开头两行放置分sheet 超链接，目前支持最大48个
        local_check_index_cell_coordinate = self.excel_col_num_to_name(local_check_index_cell_mod) + str(local_check_index_cell_quotient)
        # all sheet 超链接到各个check sheet
        worksheet_all.write_url(local_check_index_cell_coordinate, 'internal:all!A' + str(self.checkall_counter-1))
        worksheet_all.write(local_check_index_cell_coordinate, check_list, hyperlink_local_check_color)

        header_list = self.rules_json_load_dict[check_list]['header']
        for each_header in header_list:
            worksheet.write(2, count, each_header, head_color)
            #高亮表头
            worksheet_all.write(self.checkall_counter-1, count, each_header, head_color)
            count += 1
        # check表中匹配结果标注
        sheet_count = 0
        for each_hight_light_position in high_light:
            bg_level_color = eval('conf.HIGH_LIGHT_BG_COLOR_' + self.customer)[int(level_list[sheet_count])]
            font_level_color = eval('conf.HIGH_LIGHT_FONT_COLOR_' + self.customer)[int(level_list[sheet_count])]
            high_light_color = workbook.add_format({'bg_color': bg_level_color, 'font_color': font_level_color, 'bold': True})
            worksheet.conditional_format(each_hight_light_position, {'type': 'no_blanks', 'format': high_light_color})
            sheet_count += 1

        #总check表中匹配结果标注
        modify_high_light = self.modify_high_light_list(high_light_list=high_light,addend=self.checkall_counter-self.check_sheet_first_line)
        all_sheet_count = 0
        for each_modify_hight_light_position in modify_high_light:
            bg_level_color = eval('conf.HIGH_LIGHT_BG_COLOR_' + self.customer)[int(level_list[all_sheet_count])]
            font_level_color = eval('conf.HIGH_LIGHT_FONT_COLOR_' + self.customer)[int(level_list[all_sheet_count])]
            high_light_color = workbook.add_format({'bg_color': bg_level_color, 'font_color': font_level_color, 'bold': True})
            worksheet_all.conditional_format(each_modify_hight_light_position, {'type': 'no_blanks', 'format': high_light_color})
            all_sheet_count += 1
        write_log("excel {} sheet has been generated ，total {} rows".format(check_list,check_result_df_sheet_row), "green")

        if self.current_index in self.especial_indexes:
            chart_index = re.search('_chart\.',self.current_index)
            if chart_index is not None:
                chart_json= re.search('.*_',self.current_index).group()[:-1]+".json"
                chart_dict = self.open_json_dict(self.chart_json_dir, chart_json)
                self.excel_chart(workbook=workbook, worksheet=worksheet,worksheet_all=worksheet_all, sheet_name=check_list, df_row_number=check_result_df_sheet_row,df_col_number=check_result_df_sheet_col,chart_dict=chart_dict, line_number=chart_dict['line_number'])

        # check all sheet 行数定位
        self.checkall_counter = self.checkall_counter + check_result_df_sheet_row + 4


    def filename_time(self, filename, ext):
        # 输出文件增加时间自动命名
        year = strftime("%Y", localtime())
        mon = strftime("%m", localtime())
        day = strftime("%d", localtime())
        hour = strftime("%H", localtime())
        min = strftime("%M", localtime())
        sec = strftime("%S", localtime())
        # return (filename + '-' + year + mon + day + '-' + hour + min + sec + ext)
        syslog_filename = filename + '-' + year + mon + day + '-' + hour + min + sec + ext
        return syslog_filename

    #excle 数值转换为列字符
    def excel_col_num_to_name(self,colnum):
        if type(colnum) is not int:
            return colnum
        str = ''
        while (not (colnum // 26 == 0 and colnum % 26 == 0)):
            temp = 25
            if (colnum % 26 == 0):
                str += chr(temp + 65)
            else:
                str += chr(colnum % 26 - 1 + 65)
            colnum //= 26
        # 倒序输出拼写的字符串
        return str[::-1]

    def excel_col_name_to_num(self,colname):
        if type(colname) is not str:
            return colname

        col = 0
        power = 1

        for i in range(len(colname) - 1, -1, -1):
            ch = colname[i]

            col += (ord(ch) - ord('A') + 1) * power

            power *= 26

        return col

    #构造excel 字段记录
    def high_light_list(self,result_list,row_number):
        high_light_list = []
        for each_result in result_list:
            cell_position = each_result+str(row_number)
            high_light_list.append(cell_position)
        return high_light_list

    # 构造excel 字段偏移记录
    def modify_high_light_list(self,high_light_list,addend):
        modify_high_light_list = []
        for each_high_light in high_light_list:
            modify_number = int(re.search('\d+',each_high_light).group()) + addend
            modify_cell_position = re.sub("\d+", str(modify_number),each_high_light )
            modify_high_light_list.append(modify_cell_position)
        return modify_high_light_list

    # 从字符串中获取数字
    def get_num_from_str(self,content):
        match_result = re.search("\d+\.?(\d+)*", content)
        if match_result is None:
            return None
        else:
            return (match_result.group())

    def str_to_date (self,str_time):
        try:
            date = parse(str_time)
            return date.date()
        except Exception as e:
            return None

    def get_es_indexes(self,es_ip, es_port,re_pattern,customer,ex_indexes_list):
        try:
            hosts = []
            hosts.append({'host': es_ip, 'port': es_port})
            connection_pool = Transport(hosts, connection_class=RequestsHttpConnection).connection_pool
            connection = connection_pool.get_connection()
            url = '/_cat/indices?index=hc.' + customer + '*'
            #url = '/_cat/indices?index=hc.' + '4838'+ '*'
            status, headers, data = connection.perform_request('GET', url)
            all_indexes_list = re.findall(re_pattern, data)
            if all_indexes_list != []:
                check_indexs_list = list(set(all_indexes_list) - set(ex_indexes_list))
                check_indexs_list.sort()
                return check_indexs_list
            else:
                write_log("\"{}\" customer indexes got failed by url \"{}\" ".format(self.customer, url), "purple_red")
                write_log("\"{}\" customer indexes got failed by url \"{}\" ".format(self.customer, url),
                          log_name=self.log_error_name, no_print=True)
                self.error_tag = True
                exit(3)
        except Exception as e:
            write_log("\"{}\" customer indexes got failed by url \"{}\" ".format(self.customer,url),"purple_red")
            write_log("error message \"{}\" ".format(e), "red")
            self.log_error_name = filename_time(filename=log_error_filename_prefix, ext='.txt')
            write_log("\"{}\" customer indexes got failed by url \"{}\" ".format(self.customer,url),log_name=self.log_error_name, no_print=True)
            self.error_tag = True
            exit(3)

    def excel_chart(self,workbook, worksheet,worksheet_all, sheet_name, df_row_number,df_col_number,chart_dict, line_number):
        '''
        chart_col.add_series({
        'name': '=process!$A$2:$C$2',
        'categories': '=process!$D$1:$H$1',
        'values':   '=process!$D$2:$H$2',
        'line': {'color': 'red'},
        })
        {'name': '=process!$A$2:=0$C$2','categories': '=process!$D$2:$H$2','values': '=process!$D$2:$H$2','line': {'color': '#FFD700'},}
        '''

        count = 0
        incount = 0
        title_count = chart_dict['data_first_row']
        while count < df_row_number:
            # 每line number 创建新的chart 句柄，包括第一次循环
            if count % line_number == 0:
                chart = workbook.add_chart({'type': chart_dict['type']})
            # 取线色
            color = chart_dict['line_color_list'][count % len(chart_dict['line_color_list'])]
            # 数据位置变换
            data_location = count + chart_dict['data_first_row']
            # 生成数据
            # {'name': '=chart.iox.process.mem!$A$4:$C$4','categories': '=chart.iox.process.mem!$N$4:$R$4','values': '=chart.iox.process.mem!$H$4:$L$4','line': {'color': '#FFD700'},'data_labels': {'value': True,'position': 'below','border':{'color':'red'},'fill':{'color':'yellow'}},}
            series = "{\'name\': \'=" + sheet_name + "!$" + chart_dict['line_name_first'] + "$" + str(
                data_location) + ":$" + chart_dict['line_name_last'] + "$" + str(
                data_location) + "\'," + "\'categories\': \'=" + sheet_name + "!$" + chart_dict[
                         'categories_first'] + "$" + str(data_location) + ":$" + chart_dict[
                         'categories_last'] + "$" + str(
                data_location) + "\'," + "\'values\': \'=" + sheet_name + "!$" + chart_dict['value_first'] + "$" + str(
                data_location) + ":$" + chart_dict['value_last'] + "$" + str(
                data_location) + "\'," + "\'line\': {\'color\': \'" + color + "\',\'width\': 4},\'data_labels\': {\'value\': True,\'position\': \'below\',\'font\': {\'name\': \'Consolas\',\'color\': \'#008B8B\',\'size\': 15}},\'marker\': {\'type\': \'square\',\'size\': 8,\'border\': {\'color\': \'red\'},\'fill\': {\'color\':\'yellow\'}},}"
            chart.add_series(eval(series))
            # 每到line number 创建chart图
            if (count + 1) % line_number == 0 or count == (df_row_number - 1):
                #excel 起始列名转为数字
                back_top_col_number = self.excel_col_name_to_num(colname=chart_dict['back_link_first_col'])
                back_top_row_number = int(df_row_number+chart_dict['height']/20+11)
                # back top location
                back_top_location = chart_dict['back_link_first_col'] + str(
                    back_top_row_number + incount * chart_dict['back_link_first_step'])
                # back data location
                back_data_location = self.excel_col_num_to_name(colnum=back_top_col_number+1) + str(
                    back_top_row_number  + incount * chart_dict['back_link_first_step'])
                # back shee all data location
                back_sheet_all_data_location = self.excel_col_num_to_name(colnum=back_top_col_number+2) + str(
                    back_top_row_number  + incount * chart_dict['back_link_first_step'])
                # back shee all top location
                back_sheet_all_top_location = self.excel_col_num_to_name(colnum=back_top_col_number + 3) + str(
                    back_top_row_number + incount * chart_dict['back_link_first_step'])
                # chart link location
                to_link_first_col = self.excel_col_num_to_name(df_col_number+1)
                chart_link_location = to_link_first_col + str(
                    chart_dict['to_link_first_row'] + incount * line_number)
                #all sheet chart link location
                sheet_all_chart_link_location = to_link_first_col + str(
                    self.checkall_counter + 1 + incount * line_number)
                # 插入软链接
                # back top
                hyperlink_top_color = workbook.add_format(
                    {'fg_color': '#00008B', 'font_color': '#FFFAFA', 'bold': True})
                worksheet.write_url(back_top_location, 'internal:'+ sheet_name +'!A1')
                worksheet.write(back_top_location, "top", hyperlink_top_color)
                # back data
                hyperlink_top_color = workbook.add_format(
                    {'fg_color': '#FF7F50', 'font_color': '#98FB98', 'bold': True})
                worksheet.write_url(back_data_location, 'internal:'+ sheet_name+'!' + chart_link_location)
                worksheet.write(back_data_location, "data" + str(incount + 1), hyperlink_top_color)
                # back all sheet data
                hyperlink_top_color = workbook.add_format(
                    {'fg_color': '#66CDAA', 'font_color': '#FF6347', 'bold': True})
                worksheet.write_url(back_sheet_all_data_location, 'internal:all!' + sheet_all_chart_link_location)
                worksheet.write(back_sheet_all_data_location, "all data" + str(incount + 1), hyperlink_top_color)
                # back all sheet top
                hyperlink_top_color = workbook.add_format(
                    {'fg_color': '#4682B4', 'font_color': '#00FF7F', 'bold': True})
                worksheet.write_url(back_sheet_all_top_location, 'internal:all!A1')
                worksheet.write(back_sheet_all_top_location, "all top" , hyperlink_top_color)
                # to_link
                hyperlink_chart_color = workbook.add_format(
                    {'fg_color': '#9932CC', 'font_color': 'white', 'bold': True})
                worksheet.write_url(chart_link_location, 'internal:'+ sheet_name+'!' + back_data_location)
                worksheet.write(chart_link_location, "to chart" + str(incount + 1), hyperlink_chart_color)
                # sheet_all_to_link
                hyperlink_chart_color = workbook.add_format(
                    {'fg_color': '#9932CC', 'font_color': 'white', 'bold': True})
                worksheet_all.write_url(sheet_all_chart_link_location, 'internal:'+ sheet_name+'!' + back_data_location)
                worksheet_all.write(sheet_all_chart_link_location, "to chart" + str(incount + 1), hyperlink_chart_color)

                location = chart_dict['first_col'] + str(
                    (df_row_number + 9 + (incount * chart_dict['step_rows'])))
                #chart.set_title({'name': chart_dict['title'] + ' Chart' + str(incount + 1)})
                chart.set_title({'name':'chart.iox.process.mem!$A$'+str(title_count)+':$C$'+str(title_count),'name_font':{'color':'#6A5ACD','size':25,'bold':True}}),
                chart.set_x_axis({'name': chart_dict['title'] + ' Chart' + str(incount + 1),'name_font':{'color':'#CD5C5C','size':18,'bold':True}})
                chart.set_y_axis({'name': chart_dict['y_name'],'name_font':{'color':'#2E8B57','size':18,'bold':True}})
                chart.set_size({'width': chart_dict['width'], 'height': chart_dict['height']})
                chart.set_legend({'position': 'top'})
                chart.set_style(chart_dict['style'])
                worksheet.insert_chart(location, chart, {'x_offset': 25, 'y_offset': 10})
                incount += 1
                title_count = title_count + line_number

            count += 1

    @retry(stop_max_attempt_number=5, wait_random_min=10000, wait_random_max=50000)
    def send_mail(self,smtphost, mailuser, mailpass, sender, receiver, subject, content, attachment):

        body = MIMEText(content, _subtype="plain")
        msg = MIMEMultipart()
        msg["To"] = ";".join(receiver)
        msg["From"] = sender
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg.attach(body)

        for each_attachment in attachment:
            msg.attach(self.mail_attach(each_attachment))
        try:
            server = smtplib.SMTP()
            server.set_debuglevel(1)
            server.connect(smtphost)
            #server.login(mailUser,mailPass)
            server.sendmail(sender, receiver, msg.as_string())
            server.close()
            attach_files =""
            for attach in attachment:
                attach_files = attach_files + " " + attach

            write_log("mail with \"{}\" attachment has been sent".format(attach_files), "blue")
            return True
        except Exception as e:
            write_log("email failed , retry".format(), "purple_red")
            write_log("error message \"{}\" ".format(e), "red")
            raise ValueError("mail retry")

    def main(self):

        copy_info = '''
           _____                    _____                    _____                    _____          
          /\    \                  /\    \                  /\    \                  /\    \         
         /::\    \                /::\    \                /::\____\                /::\    \        
        /::::\    \              /::::\    \              /:::/    /               /::::\    \       
       /::::::\    \            /::::::\    \            /:::/    /               /::::::\    \      
      /:::/\:::\    \          /:::/\:::\    \          /:::/    /               /:::/\:::\    \     
     /:::/__\:::\    \        /:::/__\:::\    \        /:::/____/               /:::/  \:::\    \    
    /::::\   \:::\    \       \:::\   \:::\    \      /::::\    \              /:::/    \:::\    \   
   /::::::\   \:::\    \    ___\:::\   \:::\    \    /::::::\    \   _____    /:::/    / \:::\    \  
  /:::/\:::\   \:::\    \  /\   \:::\   \:::\    \  /:::/\:::\    \ /\    \  /:::/    /   \:::\    \ 
 /:::/__\:::\   \:::\____\/::\   \:::\   \:::\____\/:::/  \:::\    /::\____\/:::/____/     \:::\____\ 
 \:::\   \:::\   \::/    /\:::\   \:::\   \::/    /\::/    \:::\  /:::/    /\:::\    \      \::/    /
  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/  \/____/ \:::\/:::/    /  \:::\    \      \/____/ 
   \:::\   \:::\    \       \:::\   \:::\    \               \::::::/    /    \:::\    \             
    \:::\   \:::\____\       \:::\   \:::\____\               \::::/    /      \:::\    \            
     \:::\   \::/    /        \:::\  /:::/    /               /:::/    /        \:::\    \           
      \:::\   \/____/          \:::\/:::/    /               /:::/    /          \:::\    \          
       \:::\    \               \::::::/    /               /:::/    /            \:::\    \         
        \:::\____\               \::::/    /               /:::/    /              \:::\____\        
         \::/    /                \::/    /                \::/    /                \::/    /        
          \/____/                  \/____/                  \/____/                  \/____/         
          

        Elasticsearch Devices Health Check For CU, Version 1.00 (Build at September 1,2020)
        Author: Jing <jiwang3@cisco.com>
                Customer Experience, Cisco China
        Usage : python es_hc -c [customer_name] -i [index_name_list] -q [query_file] -r [rules_file]
                '''
        start_time = time.time()  # 开始时间
        year_month = datetime.datetime.now().strftime('%Y.%m')
        argParser = argparse.ArgumentParser()
        #argParser.add_argument("-c", "--customer",help="customer name", default="9929")
        argParser.add_argument("-c", "--customer", help="customer name")
        argParser.add_argument("-q", "--query_file", help="query json file")
        argParser.add_argument("-i", "--index_name_list", help="es index name list")
        argParser.add_argument("-r", "--rules_file", help="check json file")

        args = argParser.parse_args()

        self.customer = args.customer
        #self.customer = '169'
        if self.customer == None:
            write_log(copy_info.format(), colour="blue", skip=True)
            exit(1)

        #定义错误log文件名
        try:
            es_ip = eval('conf.ES_IP_' + self.customer)
            es_port = eval('conf.ES_PORT_' + self.customer)
            # 判断ES服务器连通性
            self.delimiter = eval('conf.RULES_JSON_DELIMITER_' + self.customer)
            log_error_filename_prefix = eval('conf.LOG_ERROR_NAME_PREFIX_' + self.customer)
            self.log_error_name = filename_time(filename=log_error_filename_prefix, ext='.txt')
            self.log_error_tag = eval('conf.LOG_ERROR_TAG_' + self.customer)
            es_search_type = eval('conf.ES_SEARCH_TYPE_' + self.customer)
            es_scroll = eval('conf.ES_SCROLL_' + self.customer)
            es_size = eval('conf.ES_SIZE_' + self.customer)
            es_timeout = eval('conf.ES_TIMEOUT_' + self.customer)
            self.chart_json_dir = eval('conf.CHART_JSON_DIR_' + self.customer)
            self.especial_indexes = eval('conf.ESPECIAL_INDEX_NAME_' + self.customer)
            query_json_dir = eval('conf.QUERY_JSON_DIR_' + self.customer)
            if args.query_file == None:
                query_json = eval('conf.QUERY_JSON_' + self.customer)
            else:
                query_json = args.query_file
            rules_json_dir = eval('conf.RULES_JSON_DIR_' + self.customer)
            if args.rules_file == None:
                rules_json = eval('conf.RULES_JSON_' + self.customer)
            else:
                rules_json = args.rules_file
            es_exclude_indexes_list = eval('conf.AUTO_EXCLUDE_INDEX_NAME_' + self.customer)
            es_auto_index_name = eval('conf.AUTO_INDEX_NAME_' + self.customer)
            if args.index_name_list != None:
                es_indexs = args.index_name_list.split(',')
            elif eval('conf.AUTO_INDEX_NAME_SWITCH_' + self.customer) == "on":
                #index_postfix = str(datetime.datetime.now().year)+"."+str(datetime.datetime.now().month)
                #es_indexs = [each_es_index + index_postfix for each_es_index in eval('conf.AUTO_INDEX_NAME_' + self.customer)]
                es_indexs = self.get_es_indexes(es_ip, es_port, es_auto_index_name, self.customer, es_exclude_indexes_list)
            else:
                es_indexs = eval('conf.INDEX_NAME_' + self.customer)
            output_dir = eval('conf.RESULT_DIR_' + self.customer)
            output_excel = eval('conf.RESULT_XLSX_NAME_PREFIX_' + self.customer)
            es_log_separator = eval('conf.ES_HC_SEPARATOR_' + self.customer)
            sort_col = eval('conf.SORT_COL_NAME_' + self.customer)
            mail_host = eval('conf.MAIL_HOST_' + self.customer)
            mail_user = eval('conf.MAIL_USER_' + self.customer)
            mail_pass = eval('conf.MAIL_PASS_' + self.customer)
            mail_from = eval('conf.MAIL_FROM_' + self.customer)
            mail_to = eval('conf.MAIL_TO_' + self.customer)
            mail_title = eval('conf.MAIL_TITLE_' + self.customer)
            mail_content = eval('conf.MAIL_CONTENT_' + self.customer)
        except Exception as e:
            write_log("\"{}\" customer parameters are not defined in the conf file ".format(self.customer),"purple_red")
            write_log("error message \"{}\" ".format(e), "red")
            write_log("\"{}\" customer parameters are not defined in the conf file ".format(self.customer), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            exit(1)

        self.log_error_name = filename_time(filename=log_error_filename_prefix, ext='.txt')
        #显示程序运行标志
        write_log(es_log_separator.format(), "yellow", skip=True)
        #定义输出文件名
        time_filename = self.filename_time(output_excel, ".xlsx")
        #设置程序发生错误标志
        self.error_tag = False
        path_time_filename = sys.path[0] + output_dir + time_filename
        self.has_conf(es_ip, es_port)
        self.writer = pd.ExcelWriter(path_time_filename, engine='xlsxwriter')
        write_log("{} es hc process starting ".format(self.customer),"blue")
        self.open_rules_json(rules_json_dir, rules_json)#打开rules json文件，放到句柄中
        self.index_count = 0
        self.index_with_data_count = 0
        self.checkall_counter = eval('conf.CHECKALL_SHEET_FIRST_ROW_'+ self.customer)
        self.check_sheet_first_line = eval('conf.CHECK_SHEET_FIRST_LINE_' + self.customer)
        self.current_index =""
        #index 处理循环
        for each_es_index in es_indexs:
            #print (each_es_index)
            self.current_index = each_es_index
            self.index_open_success = True
            check_list = re.search('_(\S+)_', each_es_index).group(1)
            index_name, es_query_result = self.el2json(query_json_dir,query_json, es_ip, es_port, es_search_type, es_scroll, es_size, es_timeout, each_es_index)
            #index 打开成功后进行后续处理
            if self.index_open_success is True:
                check_result_df,high_light,level_list = self.dict2dataframe(es_query_result,check_list=check_list,sort_col=sort_col)
                df_is_empty = re.search('Empty DataFrame', str(check_result_df.isnull()))
                if df_is_empty is None:
                    #根据conf文件获得high light表格颜色
                    high_light_color_divsor = eval('conf.HIGH_LIGHT_COLOR_DIVISOR_' + self.customer)
                    fg_color = eval('conf.HIGH_LIGHT_BG_COLOR_' + self.customer+'['+ str(self.index_with_data_count % high_light_color_divsor)+']')
                    font_color = eval('conf.HIGH_LIGHT_FONT_COLOR_' + self.customer+'['+ str(self.index_with_data_count % high_light_color_divsor)+']')
                    self.df2xlsx(check_result_df = check_result_df,check_list=check_list,high_light=high_light,level_list=level_list,fg_color=fg_color,font_color=font_color)
                    self.index_with_data_count+=1
                self.index_count+=1

        try:
            # 保存关闭文件
            if self.index_with_data_count != 0:
                self.writer.save()
                self.writer.close()
                write_log("write {} file normally".format(path_time_filename), "blue")
            #return path_time_filename, summary_sheet_col, detail_sheet_col
        except Exception as e:
            write_log("error message \"{}\" ".format(e), "red")
            write_log("write {} file abnormally".format(path_time_filename), log_name=self.log_error_name,no_print=True)
            self.error_tag = True
            exit(1)

        end_time = time.time()  # 结束时间
        interval = round((end_time - start_time), 2)
        write_log("The health check data analyze total {} index, {} index with check result, took {}s".format(self.index_count,self.index_with_data_count,interval), "bluish_blue")
        #有报错，同时有过滤结果
        if self.error_tag is True and self.index_with_data_count != 0:
            write_log("The health check data process normally with error log".format(), "blue")
            exit(2)
        # 有报错，但没有过滤结果
        if self.error_tag is True and self.index_with_data_count == 0:
            write_log("The health check data process abnormally with error log".format(), "blue")
            exit(3)
        write_log("The health check data process normally".format(), "blue")
eshc().main()