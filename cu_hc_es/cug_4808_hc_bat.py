__author__ = 'jing'
import sys
from os import system
from common import write_log
from datetime import datetime



if __name__ == '__main__':

    day_Of_Week = datetime.now().isoweekday()

    cmd_hc_4808 = 'python3 '+sys.path[0]+'/es_hc.py -c 4808'+' >>/Users/boxie2/Desktop/BJ/4808/cu_hc_es/hc_log/4808_mail_log.txt'
    cmd_mail_4808 = 'python3 '+sys.path[0]+'/mail_sent.py -c 4808'+' >>/Users/boxie2/Desktop/BJ/4808/cu_hc_es/hc_log/4808_mail_log.txt'
    cmd_mail_4808_all = 'python3 ' + sys.path[0] + '/mail_sent.py -c 4808 -s all'+' >>//Users/boxie2/Desktop/BJ/4808/cu_hc_es/hc_log/4808_mail_log.txt'
    cmd_mail_4808_hc = 'python3 ' + sys.path[0] + '/mail_sent.py -c 4808 -s hc'+' >>/Users/boxie2/Desktop/BJ/4808/cu_hc_es/hc_log/4808_mail_log.txt'
    cmd_mail_4808_log = 'python3 ' + sys.path[0] + '/mail_sent.py -c 4808 -s log'+' >>/Users/boxie2/Desktop/BJ/4808/cu_hc_es/hc_log/4808_mail_log.txt'

    result = system(cmd_hc_4808)
    if result == 0:# exit 0
        a = system(cmd_mail_4808_hc)
    elif result == 256: # exit 1
        a = system(cmd_mail_4808)
    elif result == 512: # exit2
        a = system(cmd_mail_4808_all)
    elif result == 768:# exit3
        a = system(cmd_mail_4808_log)
    else:
        write_log("cuii HC generation error!".format(), "purple_red")



