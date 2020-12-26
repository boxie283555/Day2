__author__ = 'jing'

# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE,formatdate
from email import encoders
import mimetypes
from retrying import retry
import argparse
import os
import sys
from common import write_log, latest_filename, filename_time
import conf
import datetime

def mail_attach(filename):
    try:
        fd = open(filename,"rb")
    except Exception as e:
        write_log("error message \"{}\" ".format(e), "red")
        write_log("Failed to open file \"{}\" ".format(filename), "purple_red")
        exit(1)


    #print ('mail attachemt is '+ os.path.basename(filename))
    mimetype,mimeencoding = mimetypes.guess_type(filename)
    if mimeencoding or (mimetype is None):
        mimetype = "application/octet-stream"
    maintype,subtype = mimetype.split("/")

    if maintype == "text":
        retval = MIMEText(fd.read(),'plain','utf-8')
    else:
        retval = MIMEBase(maintype,subtype)
        retval.set_payload(fd.read())
        encoders.encode_base64(retval)
    retval.add_header("Content-Disposition","attachment",filename = os.path.basename(filename))
    fd.close()
    return retval

@retry(stop_max_attempt_number=5, wait_random_min=10000, wait_random_max=50000)
def send_mail(smtphost,mailuser,mailpass,sender,receiver,subject,content,attachment):

    body = MIMEText(content,_subtype = "plain")
    msg = MIMEMultipart()
    msg["To"] = ";".join(receiver)
    msg["From"] = sender
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg.attach(body)


    for _attach in attachment:
        msg.attach(mail_attach(_attach))
    try:
        server = smtplib.SMTP()
        #server.set_debuglevel(1)
        server.connect(smtphost)
        #server.login(mailUser,mailPass)
        server.sendmail(sender,receiver,msg.as_string())
        server.close()
        attach_files = ""
        for attach in attachment:
            attach_files = attach_files + " " + attach
        write_log("mail with \"{}\" attachment has been sent".format(attach_files), "blue")
        return True
    except Exception as e:
        write_log("email failed , retry".format(), "red")
        write_log("error message \"{}\" ".format(e), "purple_red")
        raise ValueError("mail retry")
        #return False





def mail_send():

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-c", "--customer", help="customer name")
    argParser.add_argument("-s", "--sendfile", help="which file be send,all or log or hc")
    argParser.add_argument("-m", "--mainbody", help="mail content")

    args = argParser.parse_args()
    customer = args.customer = args.customer
    try:
        query_result_dir = eval('conf.RESULT_DIR_' + customer)
        query_result = eval('conf.RESULT_XLSX_NAME_PREFIX_'+ customer)
        error_log_dir = eval('conf.LOG_' + customer)
        error_log = eval('conf.LOG_ERROR_NAME_PREFIX_' + customer)
        mail_host = eval('conf.MAIL_HOST_' + customer)
        mail_user = eval('conf.MAIL_USER_' + customer)
        mail_pass = eval('conf.MAIL_PASS_' + customer)
        mail_from = eval('conf.MAIL_FROM_' + customer)
        mail_to = eval('conf.MAIL_TO_' + customer)
        mail_title = eval('conf.MAIL_TITLE_' + customer)
        if args.mainbody is not None:
            mail_content = args.mainbody
        else:
            mail_content = eval('conf.MAIL_CONTENT_' + customer)
    except Exception as e:
        write_log("\"{}\" customer parameters are not defined in the conf file ".format(customer), "purple_red")
        write_log("error message \"{}\" ".format(e), "red")
        exit(1)

    TODAY = str(datetime.date.today())
    hc_latest_result_file = latest_filename(filename=query_result, dir=sys.path[0] + query_result_dir)
    log_error_latest_file = latest_filename(filename=error_log, dir=sys.path[0] + error_log_dir)

    mail_attachments = []
    if args.sendfile == 'hc':
        if hc_latest_result_file == None:
            write_log("{} hc result file not found".format(customer), "purple_red")
            exit(1)
        mail_attachments.append(hc_latest_result_file)
    elif args.sendfile == 'log':
        if log_error_latest_file == None:
            write_log("{} error log file not found".format(customer), "purple_red")
            exit(1)
        mail_content = 'To Whom It May Concern:' + '\n' + '##### '+ customer + ' '+TODAY +' health check running abnormal , please check error log #####' + '\n' + formatdate(
            localtime=1) + '\n' + 'Hope everything goes well'
        mail_attachments.append(log_error_latest_file)
    elif args.sendfile == 'all':
        if hc_latest_result_file == None or log_error_latest_file == None :
            write_log("{} hc result file or error log file not found".format(customer), "purple_red")
            exit(1)
        mail_attachments.append(hc_latest_result_file)
        mail_attachments.append(log_error_latest_file)
    else:
        mail_content = 'To Whom It May Concern:'+'\n'+'##### '+ customer + ' '+TODAY +' health check result normal #####'+'\n'+formatdate(localtime = 1)+'\n'+'Hope everything goes well'




    send_mail(mail_host, mail_user, mail_pass, mail_from, mail_to, mail_title, mail_content, mail_attachments)



if __name__ == '__main__':

    mail_send()







