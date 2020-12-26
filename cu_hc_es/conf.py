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

#***************xxx***************************

ES_HC_SEPARATOR_xxx = '''
888    888 888d88PY88b 
888    888 888    888 
8888888888 888        
888    888 888        
888    888 888    888 
888    888 Y88b  d88P 
888    888  "Y8888P"  
       '''

ES_IP_xxx = "x.x.x.x"
ES_PORT_xxx = "9200"
ES_SEARCH_TYPE_xxx = "scan"
ES_SCROLL_xxx = "5m"
ES_SIZE_xxx = "10000"
ES_TIMEOUT_xxx = 3600
CUSTOMER_NAME_xxx = "xxx"
LOG_xxx = "/hc_log/"
LOG_ERROR_NAME_PREFIX_xxx = "hc_xxx_error_log"
LOG_ERROR_TAG_xxx = "Hostname"
AUTO_INDEX_NAME_SWITCH_xxx = "on"
AUTO_EXCLUDE_INDEX_NAME_xxx = ["hc.xxx_iox.process.mem_"+YEAR_MONTH,"hc.xxx_a9k.iox.process.mem_"+YEAR_MONTH,"hc.xxx_a9k.iox.install.active.base_"+YEAR_MONTH,"hc.xxx_a9k.iox.install.commit_"+YEAR_MONTH,"hc.xxx_a9k.iox.install.active.smu_"+YEAR_MONTH,"hc.xxx.test_iox.process.mem_"+YEAR_MONTH,"hc.xxx_graph.iox.process.mem_"+YEAR_MONTH,'hc.xxx_a9k.iox.install.active_'+YEAR_MONTH]
INDEX_NAME_xxx = ["hc.xxx_a9k.iox.fans_"+YEAR_MONTH]
AUTO_INDEX_NAME_xxx = "hc.xxx_\\S*"+YEAR_MONTH
ESPECIAL_INDEX_NAME_xxx = ["hc.xxx_chart.iox.process.mem_"+YEAR_MONTH]
INDEX_TYPE_xxx = "_doc"
QUERY_JSON_DIR_xxx = "/query_json/"
QUERY_JSON_xxx = "hc_xxx_query_date.json"
CHART_JSON_DIR_xxx = "/chart_json/"
RULES_JSON_DIR_xxx = "/rules_json/"
RULES_JSON_xxx = "rules_xxx.json"
RULES_JSON_DELIMITER_xxx = {"Ω","α","β","γ","δ","ε","ζ","η","θ","ι","κ","λ","μ","ν","ξ","ο","π","ρ","σ","τ","υ","φ","χ","ψ","ω","‖"}
RESULT_DIR_xxx = "/hc_results_xxx/"
RESULT_XLSX_NAME_PREFIX_xxx = "hc_xxx"
SORT_COL_NAME_xxx = ["Hostname","Timestamp","Platform_type"]
HIGH_LIGHT_BG_COLOR_xxx = ["#DB7093","#479ac7","#98FB98","#FFDAB9"]
HIGH_LIGHT_FONT_COLOR_xxx = ["#FFD700","#FFFFFF","#808080","#00BFFF"]
HIGH_LIGHT_COLOR_DIVISOR_xxx = 4
CHECKALL_SHEET_FIRST_ROW_xxx = 9
CHECKALL_SHEET_HYPERLINK_xxx = 16
CHECK_SHEET_FIRST_LINE_xxx = 3
CHECKALL_SHEET_LOCAL_HYPERLINK_FIRST_ROW_xxx = 4
MAIL_HOST_xxx = ""
MAIL_USER_xxx = ""
MAIL_PASS_xxx = ""
MAIL_FROM_xxx = ""
MAIL_TO_xxx = [""]
MAIL_TITLE_xxx = "CUII DAY2 HEALTH CHECK"
MAIL_CONTENT_xxx = 'To Whom It May Concern:'+'\n'+'##### xxx '+TODAY +' health check result file has been generated, please find it in attachment #####'+'\n'\
                    +'You can also get it from the web link: '+'http://x.x.x.x/hc_results_xxx/'+'\n'+formatdate(localtime = 1)+'\n'+'Hope everything goes well'