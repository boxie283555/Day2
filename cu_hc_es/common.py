#!/usr/bin/env python3
# coding: utf-8
#python -m py_compile cug_log_es_eng_scroll_scan.py
"""
共有的方法
"""

import sys
import io
import re


def setup_io():  # 设置默认屏幕输出为utf-8编码
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)


setup_io()

import os
import time
import conf
import socket
import subprocess
import ipaddress
from multiprocessing import cpu_count
from time import strftime, localtime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def write_log(content, colour='white',log_name='es_hc_log.txt',skip=False,no_print = False):
    """
    写入日志文件
    :param content: 写入内容
    :param colour: 颜色
    :param skip: 是否跳过打印时间
    :return:
    """
    # 颜色代码
    colour_dict = {
        'red': 31,  # 红色
        'green': 32,  # 绿色
        'yellow': 33,  # 黄色
        'blue': 34,  # 蓝色
        'purple_red': 35,  # 紫红色
        'bluish_blue': 36,  # 浅蓝色
        'white': 37,  # 白色
    }
    choice = colour_dict.get(colour)  # 选择颜色
    log_path = sys.path[0] + '/hc_log' + '/' + log_name

    path = os.path.join(BASE_DIR, log_path)  # 日志文件
    with open(path, mode='a+', encoding='utf-8') as f:
        if skip is False:  # 不跳过打印时间时
            content = time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + content

        info = "\033[1;{};1m{}\033[0m".format(choice, content)
        if no_print is False:
            print(info)
        f.write(content + "\n")


def execute_linux2(cmd, timeout=10, skip=False):
    """
    执行linux命令,返回list
    :param cmd: linux命令
    :param timeout: 超时时间,生产环境, 特别卡, 因此要3秒
    :param skip: 是否跳过超时
    :return: list
    """
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    # print(p)
    # timeout = 1  # 超时时间
    t_beginning = time.time()  # 开始时间
    # seconds_passed = 0  # 执行时间
    while True:
        if p.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            p.terminate()
            # raise TimeoutError(cmd, timeout)
            if not skip:
                # self.res.code = 500
                # print('命令: {},执行超时!'.format(cmd))
                write_log('错误, 命令: {},本地执行超时!'.format(cmd), "red")
                # return self.res.__dict__
                return False
                # return '命令: {},执行超时!'.format(cmd)

    # result = p.stdout.read().decode('utf-8').strip()  # 命令运行结果
    # print("result",result)
    # self.res.data = result
    # return self.res.__dict__
    result = p.stdout.readlines()
    return result


def valid_ip(ip):
    """
    验证ip是否有效,比如192.168.1.256是一个不存在的ip
    :return: bool
    """
    try:
        # 判断 python 版本
        if sys.version_info[0] == 2:
            ipaddress.ip_address(ip.strip().decode("utf-8"))
        elif sys.version_info[0] == 3:
            # ipaddress.ip_address(bytes(ip.strip().encode("utf-8")))
            ipaddress.ip_address(ip)

        return True
    except Exception as e:
        print(e)
        return False


def check_tcp(ip, port, timeout=1):
    """
    检测tcp端口
    :param ip: ip地址
    :param port: 端口号
    :param timeout: 超时时间
    :return: bool
    """
    flag = False
    try:
        socket.setdefaulttimeout(timeout)  # 整个socket层设置超时时间
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (str(ip), int(port))
        status = cs.connect_ex((address))  # 开始连接
        cs.settimeout(timeout)

        if not status:
            flag = True

        return flag
    except Exception as e:
        print(e)
        return flag

def latest_filename(filename,dir):
    result_dir = (dir)
    allFile =  os.listdir(result_dir)
    whatFile = re.compile(filename,re.IGNORECASE)
    fileGroup = [b for b in allFile if whatFile.search(b)]
    fileGroup.sort(key=lambda fn: os.path.getmtime(result_dir+"/"+fn) if not os.path.isdir(result_dir+"/"+fn) else 0)

    if len(fileGroup) == 0:
        write_log("under the directory \"{} \", no files matching \"{}\" were found:(".format(dir, filename), "green")
        return None
    else:
        write_log("under the directory \"{}\", like  \"{}\" is found , the latest file is \"{}\":)".format(dir, filename , fileGroup[-1]), "green")
        return dir+fileGroup[-1]

def filename_time(filename, ext):
    # 输出文件自动命名
    year = strftime("%Y", localtime())
    mon = strftime("%m", localtime())
    day = strftime("%d", localtime())
    hour = strftime("%H", localtime())
    min = strftime("%M", localtime())
    sec = strftime("%S", localtime())
    return (filename + '-' + year + mon + day + '-' + hour + min + sec + ext)

COROUTINE_NUMBER = cpu_count()  # 协程池数量，根据cpu核心数来开，避免cpu飙高