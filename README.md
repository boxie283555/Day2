# Day2
     这个项目主要目的是检查Cisco NCS，CRS设备运行状态。三种类型的设备分别有对应的检查命令，通过这些命令收集的信息，并对输出结果通过TextFSM进行结构化处理，输出到ElasticSearch数据库进行存储，并通过Kibana进行展示或通过程序中定义的检查规则，对命令采集到的异常信息进行XlS格式的输出。
     设备的登录方式为Telnet或SSH

     设备时区仅支持GMT，UTC，CST，或为其它名字的时区请Pull Request


# Day2安装步骤：
1.需要安装ElasticSearch数据库，安装方法参见其它Git文档。

2.git clone https://github.com/boxie283555/Day2.git下载软件到本地。

3.修改device.xxx.txt设备的登录信息。格式如下：

     主机名::IP::用户名::密码::cisco_xr::设备类型::cisco_xr

     #设备类型目前仅支持NCS或CRS

4.修改/etc/hosts文件，指定ES服务器的地址,格式如下：

     x.x.x.x	elastic_host

5.修改es_file_ncs_v1.conf文件，将所有字段xxx替换成项目名称

6.修改es_file_v1.conf文件，将所有字段xxx替换成项目名称

7.将ncs_index_mapping目录下的所有文件改名hc.xxx -> hc.项目名称

8.将crs_index_mapping目录下的所有文件改名hc.xxx -> hc.项目名称

9.修改主脚本文件的属性如下：

     chmod 777 run.sh #CRS主脚本

     chmod 777 run_ncs.sh #NCS主脚本

10.若检查CRS，执行./run.sh，结果数据存在hcdata_crs目录中。若检查NCS，执行./run_ncs.sh，结果数据存在hcdata_ncs目录中

11.结果报表的输出：

     修改cu_hc_es\rules_json\conf.py文件.将所有字段xxx替换成项目名称，并修改这些字段：
     ES_IP_xxx = "x.x.x.x" 
     ES_PORT_xxx = "9200"
     CUSTOMER_NAME_xxx = "xxx"
     如需要自动邮件提醒功能，修改以下字段：
     MAIL_HOST_xxx = ""
     MAIL_USER_xxx = ""
     MAIL_PASS_xxx = ""
     MAIL_FROM_xxx = ""
     MAIL_TO_xxx = [""]

12.修改cug_xxx_hc_bat.py文件，将所有字段xxx替换成项目名称。包括文件名中的XXX。增加cug_xxx_hc_bat.py的执行属性。

    

