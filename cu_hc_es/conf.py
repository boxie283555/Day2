#!/usr/bin/env python3
# coding: utf-8
"""
配置文件，用于mysql和elasticsearch
"""
import os
from email.utils import formatdate
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根目录
TODAY = str(datetime.date.today())
YESTERDAY = str(datetime.date.today() - datetime.timedelta(days=1)).replace("-", ".")
YEAR_MONTH = datetime.datetime.now().strftime('%Y.%m')

#***************4808***************************

ES_HC_SEPARATOR_4808 = '''
888    888 888d88PY88b 
888    888 888    888 
8888888888 888        
888    888 888        
888    888 888    888 
888    888 Y88b  d88P 
888    888  "Y8888P"  
       '''

ES_IP_4808 = "10.75.44.133"
ES_PORT_4808 = "9200"
ES_SEARCH_TYPE_4808 = "scan"
ES_SCROLL_4808 = "5m"
ES_SIZE_4808 = "10000"
ES_TIMEOUT_4808 = 3600
CUSTOMER_NAME_4808 = "4808"
LOG_4808 = "/hc_log/"
LOG_ERROR_NAME_PREFIX_4808 = "hc_4808_error_log"
LOG_ERROR_TAG_4808 = "Hostname"
AUTO_INDEX_NAME_SWITCH_4808 = "on"
AUTO_EXCLUDE_INDEX_NAME_4808 = ["hc.4808_iox.process.mem_"+YEAR_MONTH,"hc.4808_a9k.iox.process.mem_"+YEAR_MONTH,"hc.4808_a9k.iox.install.active.base_"+YEAR_MONTH,"hc.4808_a9k.iox.install.commit_"+YEAR_MONTH,"hc.4808_a9k.iox.install.active.smu_"+YEAR_MONTH,"hc.4808.test_iox.process.mem_"+YEAR_MONTH,"hc.4808_graph.iox.process.mem_"+YEAR_MONTH,'hc.4808_a9k.iox.install.active_'+YEAR_MONTH]
INDEX_NAME_4808 = ["hc.4808_a9k.iox.fans_"+YEAR_MONTH]
AUTO_INDEX_NAME_4808 = "hc.4808_\\S*"+YEAR_MONTH
ESPECIAL_INDEX_NAME_4808 = ["hc.4808_chart.iox.process.mem_"+YEAR_MONTH]
INDEX_TYPE_4808 = "_doc"
QUERY_JSON_DIR_4808 = "/query_json/"
QUERY_JSON_4808 = "hc_4808_query_date.json"
CHART_JSON_DIR_4808 = "/chart_json/"
RULES_JSON_DIR_4808 = "/rules_json/"
RULES_JSON_4808 = "rules_4808.json"
RULES_JSON_DELIMITER_4808 = {"Ω","α","β","γ","δ","ε","ζ","η","θ","ι","κ","λ","μ","ν","ξ","ο","π","ρ","σ","τ","υ","φ","χ","ψ","ω","‖"}
RESULT_DIR_4808 = "/hc_results_4808/"
RESULT_XLSX_NAME_PREFIX_4808 = "hc_4808"
SORT_COL_NAME_4808 = ["Hostname","Timestamp","Platform_type"]
HIGH_LIGHT_BG_COLOR_4808 = ["#DB7093","#479ac7","#98FB98","#FFDAB9"]
HIGH_LIGHT_FONT_COLOR_4808 = ["#FFD700","#FFFFFF","#808080","#00BFFF"]
HIGH_LIGHT_COLOR_DIVISOR_4808 = 4
CHECKALL_SHEET_FIRST_ROW_4808 = 9
CHECKALL_SHEET_HYPERLINK_4808 = 16
CHECK_SHEET_FIRST_LINE_4808 = 3
CHECKALL_SHEET_LOCAL_HYPERLINK_FIRST_ROW_4808 = 4
MAIL_HOST_4808 = "outbound.cisco.com"
MAIL_USER_4808 = ""
MAIL_PASS_4808 = ""
MAIL_FROM_4808 = "cx-cu-day2@cisco.com"
MAIL_TO_4808 = ["cx-cu-day2@cisco.com"]
MAIL_TITLE_4808 = "CUII DAY2 HEALTH CHECK"
MAIL_CONTENT_4808 = 'To Whom It May Concern:'+'\n'+'##### 4808 '+TODAY +' health check result file has been generated, please find it in attachment #####'+'\n'\
                    +'You can also get it from the web link: '+'http://10.75.44.133/hc_results_4808/'+'\n'+formatdate(localtime = 1)+'\n'+'Hope everything goes well'