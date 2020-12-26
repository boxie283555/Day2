__author__ = 'jing'
import sys
from os import system
from common import write_log
from datetime import datetime



if __name__ == '__main__':

    day_Of_Week = datetime.now().isoweekday()

    cmd_hc_4837 = 'python372 '+sys.path[0]+'/es_hc.py -c 4837'+' >>/usr/local/cu_hc_es/hc_log/4837_mail_log.txt'
    cmd_mail_4837 = 'python372 '+sys.path[0]+'/mail_sent.py -c 4837'+' >>/usr/local/cu_hc_es/hc_log/4837_mail_log.txt'
    cmd_mail_4837_all = 'python372 ' + sys.path[0] + '/mail_sent.py -c 4837 -s all'+' >>/usr/local/cu_hc_es/hc_log/4837_mail_log.txt'
    cmd_mail_4837_hc = 'python372 ' + sys.path[0] + '/mail_sent.py -c 4837 -s hc'+' >>/usr/local/cu_hc_es/hc_log/4837_mail_log.txt'
    cmd_mail_4837_log = 'python372 ' + sys.path[0] + '/mail_sent.py -c 4837 -s log'+' >>/usr/local/cu_hc_es/hc_log/4837_mail_log.txt'

    result = system(cmd_hc_4837)
    if result == 0:# exit 0
        a = system(cmd_mail_4837_hc)
    elif result == 256: # exit 1
        a = system(cmd_mail_4837)
    elif result == 512: # exit2
        a = system(cmd_mail_4837_all)
    elif result == 768:# exit3
        a = system(cmd_mail_4837_log)
    else:
        write_log("cuii HC generation error!".format(), "purple_red")



