# Day2
     这个项目主要目的是检查Cisco NCS，CRS设备的运行状态。每种类型的设备分别有对应的检查命令，命令收集到的信息通过TextFSM结构化处理后，存储到ElasticSearch数据库，可使用Kibana进行展示。也可通过程序中定义的检查规则，输出相应XlS格式的报表。
     设备的登录方式为Telnet或SSH

     设备时区仅支持GMT，UTC，CST，或为其它名字的时区请Pull Request

     设备的检查命令参考command开头的配置文件。

     结构化模板参考asr/ncs/crs目录下的文件。



# Day2安装步骤：
1.需要安装ElasticSearch数据库.安装方法参见其它Git文档。

2.git clone https://github.com/boxie283555/Day2.git下载软件到本地。

3.修改device.xxx.txt设备的登录信息。格式如下：

     主机名::IP::用户名::密码::cisco_xr::设备类型::cisco_xr

     #设备类型目前仅支持NCS或CRS

4.修改/etc/hosts文件，指定ES服务器的地址,格式如下：

     x.x.x.x	elastic_host

     可选修改：（使用特定的客户名称时）
     a.修改es_file_ncs_v1.conf文件，将所有字段xxx替换成项目名称

     b.修改es_file_v1.conf文件，将所有字段xxx替换成项目名称

     c.修改es_file_a9k.conf文件，将所有字段xxx替换成项目名称

     d.将ncs_index_mapping目录下的所有文件改名hc.xxx -> hc.项目名称

     e.将crs_index_mapping目录下的所有文件改名hc.xxx -> hc.项目名称

     f.将a9k_index_mapping目录下的所有文件改名hc.xxx -> hc.项目名称


5.修改主脚本文件的属性如下：

     chmod 777 run.sh #CRS主脚本

     chmod 777 run_ncs.sh #NCS主脚本

     chmod 777 run_a9k.sh #NCS主脚本


10.若检查CRS，执行./run.sh，结果数据存在hcdata_crs目录中。若检查NCS，执行./run_ncs.sh，结果数据存在hcdata_ncs目录中。若检查ASR，执行./run_a9k.sh，结果数据存在hcdata_a9k目录中

11.结果报表的输出。若在步骤4中，修改了客户名称，需要将所有字段xxx替换成项目名称，并修改这些字段：

     修改cu_hc_es\rules_json\conf.py文件.
     ES_IP_xxx = "x.x.x.x" 
     ES_PORT_xxx = "9200"
     CUSTOMER_NAME_xxx = "xxx"
     如需要自动邮件提醒功能，修改以下字段：
     MAIL_HOST_xxx = ""
     MAIL_USER_xxx = ""
     MAIL_PASS_xxx = ""
     MAIL_FROM_xxx = ""
     MAIL_TO_xxx = [""]

12.修改cug_xxx_hc_bat.py的属性，使其具有执行属性。执行cug_xxx_hc_bat.py。得到相应的xls报表。若在步骤4中，修改了客户名称，需修改cug_xxx_hc_bat.py文件，将所有字段xxx替换成项目名称。包括文件本身名命名。

    

