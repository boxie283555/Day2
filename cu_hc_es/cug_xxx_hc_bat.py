__author__ = 'Jing'
import sys
from os import system
from common import write_log
from datetime import datetime



if __name__ == '__main__':

    day_Of_Week = datetime.now().isoweekday()

    cmd_hc_xxx = 'python3 '+sys.path[0]+'/es_hc.py -c xxx'+' >> ./cu_hc_es/hc_log/xxx_mail_log.txt'
    cmd_mail_xxx = 'python3 '+sys.path[0]+'/mail_sent.py -c xxx'+' >> ./cu_hc_es/hc_log/xxx_mail_log.txt'
    cmd_mail_xxx_all = 'python3 ' + sys.path[0] + '/mail_sent.py -c xxx -s all'+' >> ./cu_hc_es/hc_log/xxx_mail_log.txt'
    cmd_mail_xxx_hc = 'python3 ' + sys.path[0] + '/mail_sent.py -c xxx -s hc'+' >> ./cu_hc_es/hc_log/xxx_mail_log.txt'
    cmd_mail_xxx_log = 'python3 ' + sys.path[0] + '/mail_sent.py -c xxx -s log'+' >> ./cu_hc_es/hc_log/xxx_mail_log.txt'

    result = system(cmd_hc_xxx)
    if result == 0:# exit 0
        a = system(cmd_mail_xxx_hc)
    elif result == 256: # exit 1
        a = system(cmd_mail_xxx)
    elif result == 512: # exit2
        a = system(cmd_mail_xxx_all)
    elif result == 768:# exit3
        a = system(cmd_mail_xxx_log)
    else:
        write_log("cuii HC generation error!".format(), "purple_red")



