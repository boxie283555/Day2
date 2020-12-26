import os
import json
import textfsm
import datetime
import time
import re

current_dir = os.getcwd()
#template_dir = current_dir + "/" + "ntc-templates/templates/" 
#command_txt_dir = current_dir + "/" + "ntc-templates/command_txt/"
 
template_dir = current_dir + "/ncs"
command_txt_dir = template_dir

def Get_data(filename):
    os.chdir(command_txt_dir) 
    input_file = open(filename, encoding='utf-8')
    raw_text_data = input_file.read()
    input_file.close()
    # print(raw_text_data)
    return raw_text_data

def Get_templete(template_name):
    os.chdir(template_dir) 
    # Run the text through the FSM. ^${hostname}[>#].*
    # The argument 'template' is a file handle and 'raw_text_data' is a 
    # string with the content from the templates\datatime.textfsm file
    template = open(template_name)
    return template

def textfsm_result_conver_to_dic_new(fsm_header_list, fsm_content):
    result = list()
    for line in fsm_content:
        # print(line)
        tmp_result_dic = dict(zip(fsm_header_list, line))

        result.append(tmp_result_dic)
    return result

def run(show_file, template_file):
    text_data = Get_data(filename=show_file)
    template = Get_templete(template_name= template_file)
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(text_data)
    res = textfsm_result_conver_to_dic_new(fsm_header_list= re_table.header, fsm_content=fsm_results)
    return res

def modify_json(filename):
    print(os.getcwd())
    os.chdir(command_txt_dir)
    try:
        with open(filename,'r') as r:
            lines=r.readlines()
    except:
          print('modify_json:{} json file does not exist.'.format(filename))
    with open(filename,'w') as w:
        print(len(lines))
        if len(lines) == 1:
            new = '{"index":{}}'+'\n'
            new_line = str((lines[0])[1:-1])
            w.write(new)
            w.write(new_line)
            w.write("\n")  
        else:
            for row in lines:  
                print("row",row)
                if row.strip().startswith("["):   
                    new = '{"index":{}}'+'\n'
                    w.write(new)                   
                    continue
                elif row.strip().startswith("},"):    
                    new1 = '}'+'\n'+'{"index":{}}'+'\n'
                    w.write(new1)
                    continue
                elif row.strip().startswith("]"):  
                    new2 = '\n'
                    w.write(new2)
                    continue
                else:
                    raw = row.strip()
                    w.write(raw.strip('\n\t'))   
            w.write("\n")  


if __name__ == '__main__':
#NCS Verified
    #show_file = "show_processes_cpu.txt"
    #show_file = "show_processes_cpu_1.txt"
    #show_file = "show_processes_cpu_2.txt"  #null
    #template_file = "cisco_ncs_show_processes_cpu.textfsm"
 
    #show_file = "show_processes_memory_location_all.txt"
    #template_file = "cisco_ncs_show_processes_memory_location_all.textfsm" 

    #show_file = "show_memory_summary_location_all.txt"
    #template_file = "cisco_ncs_show_memory_summary_location_all.textfsm"

    #show_file = "show_processes_blocked_location_all.txt"
    #template_file = "cisco_ncs_show_processes_blocked_location_all.textfsm"

    #show_file = "show_processes_aborts_location_all.txt"
    #template_file = "cisco_ncs_show_processes_aborts_location_all.textfsm"

    #template_file = "cisco_ncs_admin_show_install_active_summary.textfsm"
    #show_file= "admin_show_install_active_summary.txt"    

    #template_file = "cisco_ncs_admin_show_install_inactive_summary.textfsm"
    #show_file= "admin_show_install_inactive_summary.txt"    

    #template_file = "cisco_ncs_show_install_active_summary.textfsm"
    #show_file= "show_install_active_summary.txt"    

    #template_file = "cisco_ncs_show_install_inactive_summary.textfsm"
    #show_file= "show_install_inactive_summary.txt"    

    #template_file = "cisco_ncs_show_install_superseded_summary.textfsm"
    #show_file= "show_install_superseded_summary.txt"

    #template_file = "cisco_ncs_admin_show_platform.textfsm"
    #show_file= "admin_show_platform.txt"

    #template_file = "cisco_ncs_admin_show_platform_slice.textfsm"
    #show_file = "admin_show_platform_slice.txt"

    #template_file = "cisco_ncs_show_context_location_all.textfsm"
    #show_file = "show_context_location_all.txt"
    #show_file = "show_context_location_all_1.txt"

    #show_file= "admin_show_environment_power.txt"
    #show_file= "admin_show_environment_power_1.txt"
    show_file= "admin_show_environment_power_2.txt"
    template_file = "cisco_ncs_admin_show_environment_power.textfsm"

    #show_file= "admin_show_environment_fan_ft.txt" 
    #template_file = "cisco_ncs_admin_show_environment_fans_ft.textfsm"

    #show_file= "admin_show_environment_fan_pt.txt" 
    #template_file = "cisco_ncs_admin_show_environment_fans_pt.textfsm"

    #show_file= "admin_show_led.txt"
    #template_file = "cisco_ncs_admin_show_led.textfsm"

    #show_file= "admin_show_hw-module_fpd.txt"
    #template_file = "cisco_ncs_admin_show_hw_module_fpd.textfsm"

    #show_file= "show_ntp_status.txt"
    #template_file = "cisco_ncs_show_ntp_status.textfsm"

    #show_file= "admin_dir_harddisk_location_all.txt"
    #template_file = "cisco_ncs_admin_dir_harddisk_location_all.textfsm"

    #show_file= "admin_dir_disk0_location_all.txt"
    #template_file = "cisco_ncs_admin_dir_disk0_location_all.textfsm"

    #show_file= "admin_dir_rootfs_location_all.txt"
    #template_file = "cisco_ncs_admin_dir_rootfs_location_all.textfsm"

    #show_file= "show_placement_reoptimize.txt"
    #template_file = "cisco_ncs_show_placement_reoptimize.textfsm"

    #show_file = "show_redundancy_summary.txt"
    #template_file = "cisco_ncs_show_redundancy_summary.textfsm"

    #show_file = "admin_show_controller_fabric_plane_all_detail.txt"
    #template_file = "cisco_ncs_admin_show_controller_fabric_plane_all_detail.textfsm"

    #show_file = "admin_show_controller_fabric_plane_all_statistics.txt" 
    #template_file = "cisco_ncs_admin_show_controller_fabric_plane_all_statistics.textfsm"

    #show_file = "admin_show_controller_fabric_bundle_all_detail.txt"
    #template_file = "cisco_ncs_admin_show_controller_fabric_bundle_all_detail.textfsm"

    #template_file = "cisco_ncs_admin_show_install_superseded_summary.textfsm"
    #show_file= "admin_show_install_superseded_summary.txt"

    #show_file= "admin_show_vm.txt"
    #template_file = "cisco_ncs_admin_show_vm.textfsm"

    #show_file= "admin_show_alarms_brief.txt"
    #template_file= "cisco_ncs_admin_show_alarms_brief.textfsm"

    #show_file="admin_show_chassis.txt"
    #template_file="cisco_ncs_admin_show_chassis.textfsm"

    #show_file="admin_show_controller_fabric_link_port_s3_rx_state_down.txt"
    #template_file="cisco_ncs_admin_show_controller_fabric_link_port_s3_rx_state_down.textfsm"

    #show_file="admin_show_controller_fabric_sfe_s13_all.txt"
    #template_file="cisco_ncs_admin_show_controller_fabric_sfe_s13_all.textfsm"

    #show_file="admin_show_controller_fabric_sfe_s2_all.txt"
    #template_file="cisco_ncs_admin_show_controller_fabric_sfe_s2_all.textfsm"

    #show_file="admin_show_controller_fabric_sfe_fia_all.txt"
    #template_file="cisco_ncs_admin_show_controller_fabric_sfe_fia_all.textfsm"

    #show_file="admin_show_controller_fabric_link_port_s2_rx_state_down.txt"
    #template_file="cisco_ncs_admin_show_controller_fabric_link_port_s2_rx_state_down.textfsm"

    #show_file="show_health_sysdb_location_0_rp1_CPU0.txt"
    #template_file="show_health_sysdb.textfsm"

    #show_file="admin_show_sdr_default_sdr_pairing.txt"
    #template_file="cisco_ncs_admin_show_sdr_default_sdr_pairing.textfsm"

    #show_file="show_bgp_neighbors.txt"
    #template_file="cisco_ncs_show_bgp_neighbors.textfsm"

# ASR9K Verified

    #show_file= "admin_show_environment_fans_location_all.txt"
    #show_file= "admin_show_environment_fans_location_all_9006.txt"
    #template_file = "cisco_xr9k_admin_show_environment_fans.textfsm"

    #show_file= "4808_admin_show_environment_power-supply_location_all.txt"
    #show_file= "admin_show_environment_power-supply_location_all.txt"
    #template_file = "cisco_xr9k_admin_show_environment_power_supply.textfsm"


    #template_file = "cisco_xr9k_show_environment_leds_details_location_all.textfsm"
    #show_file= "show_environment_leds_details_location_all.txt"


    #template_file = "cisco_xr9k_admin_show_platform.textfsm"
    #show_file= "admin_show_platform.txt"


    #show_file = 'admin_show_hw-module_fpd_location_all.txt'
    #show_file = 'crs-hw-fpd.txt'
    #template_file = 'cisco_xr9k_admin_show_hw-module_fpd_location_all.textfsm'


    #show_file = 'admin_dir_disk0_location_all.txt'
    #template_file = 'cisco_xr9k_admin_dir_disk0_location_all.textfsm'

    #show_file = "admin_dir_harddisk_location_all.txt"
    #template_file = "cisco_xr9k_admin_dir_harddisk_location_all.textfsm"


    #template_file = "cisco_xr9k_admin_show_install_active_summary_base.textfsm"
    #show_file= "admin_show_install_active_summary_base.txt"

    #template_file = "cisco_xr9k_admin_show_install_active_summary_smu.textfsm"
    #show_file= "admin_show_install_active_summary_smu.txt"


    #template_file = "cisco_xr9k_admin_show_install_active_summary.textfsm"
    #show_file= "admin_show_install_active_summary.txt"

    #template_file = "cisco_xr9k_admin_show_install_inactive_summary.textfsm"
    #show_file= "admin_show_install_inactive_summary.txt"

    #template_file = "cisco_xr9k_admin_show_install_commit_summary.textfsm"
    #show_file= "admin_show_install_commit_summary.txt"

    #template_file = "cisco_xr9k_admin_show_install_superceded.textfsm"
    #show_file= "admin_show_install_superceded.txt"

    #show_file = "show_ntp_status.txt"
    #template_file = "cisco_xr9k_show_ntp_status.textfsm"

    #show_file = "admin_show_redundancy.txt"
    #template_file = "cisco_xr9k_admin_show_redundancy.textfsm"

    #show_file = "show_redundancy_sum.txt"
    #template_file = "cisco_xr9k_admin_show_redundancy_summary.textfsm"

    #show_file = "show_context_location_all.txt"
    #template_file = "cisco_xr9k_show_context_location_all.textfsm"

    #show_file = "show_processes_aborts_location_all.txt"
    #show_file = "show_processes_aborts_location_all_bak.txt"
    #template_file = "cisco_xr9k_show_processes_aborts_location_all.textfsm"

    #show_file = "show_processes_cpu.txt"
    #template_file = "cisco_xr9k_show_processes_cpu.textfsm"

    #show_file = "show_process_block_location_all.txt"
    #template_file = "cisco_xr9k_show_processes_blocked_location_all.textfsm"

    #show_file = "show_processes_memory_location_all.txt"
    #template_file = "cisco_xr9k_show_processes_memory_location_all.textfsm"

    #show_file = "4808_show_memory_summary_location_all.txt"
    #show_file = "show_memory_summary_location_all.txt"
    #template_file = "cisco_xr9k_show_memory_summary_location_all.textfsm"

    #show_file= "show_pfm_location_all.txt"
    #show_file= "4808_show_pfm_location_all.txt"

    #template_file = "cisco_xr9k_show_pfm_location_all.textfsm"


    #show_file= "show_vrf_all.txt"
    #template_file = "cisco_xr9k_sh_vrf.textfsm"


    #template_file = "cisco_xr9k_show_prm_server_tcam_summary_all_all_all.textfsm"
    #show_file= "show_prm_server_tcam_summary_all_all_all.txt"

    #template_file = "cisco_xr9k_admin_show_variables_boot_location_all.textfsm"
    #show_file= "admin_show_variables_boot_location_all.txt"

    #template_file = "cisco_xr9k_show_controllers_backplane_ethernet_links_location_0_RSPx_CPU0.textfsm"
    #show_file= "show_controllers_backplane_ethernet_links_location_0_RSP0_CPU0.txt"

    #template_file = "cisco_xr9k_show_controllers_backplane_ethernet_links_location_0_RSPx_CPU0.textfsm"
    #show_file= "show_controllers_backplane_ethernet_links_location_0_RSP1_CPU0.txt"

    #template_file = "cisco_xr9k_show_health_gsp_location_0_RSPx_CPU0.textfsm.bak"
    #show_file= "show_health_gsp_location_0_RSP1_CPU0.txt"
    #show_file= "gsp_old.txt"


    #template_file = "cisco_xr9k_show_health_gsp_location_0_RSPx_CPU0.textfsm"
    #show_file= "show_health_gsp_location_0_RSP0_CPU0.txt"

    #template_file = "cisco_xr9k_show_bgp_vrf_all_neighbors_prefix.textfsm"
    #show_file= "show_bgp_vrf_all_neighbors_prefix.txt"

    #template_file = "cisco_xr9k_show_bgp_all_neighbors_prefix.textfsm"
    #show_file= "sh_bgp_neighbors_prefix.txt"    

    #template_file = "cisco_xr9k_sh_bgp_vrf_all_neighbors_info.textfsm"
    #show_file= "sh_bgp_vrf_all_neighbors_info.txt"

    #template_file = "cisco_xr9k_show_bgp_neighbors.textfsm"
    #show_file= "show_bgp_neighbors.txt"

    #template_file = "cisco_xr9k_admin_show_environment_temperature.textfsm"
    #show_file= "admin_show_environment_temperature.txt"

    #template_file = "cisco_xr9k_show_clock.textfsm"
    #show_file= "show_clock.txt"

    #template_file = "cisco_xr9k_show_running_hostname.textfsm"
    #show_file= "show_running_config_hostname.txt"

    #template_file = "cisco_xr9k_show_inventory_rack.textfsm"
    #show_file= "show_inventory_rack.txt"
    
    output = run(show_file=show_file, template_file=template_file)
    



    print(output)
    json_data = json.dumps(output)
    os.chdir(command_txt_dir) 
    json_file = open("output.json","w")
    json_file.write(json_data)
    json_file.close()


    #modify_json("output.json")

