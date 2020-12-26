#! /bin/bash
file_date=$(date +'%m-%d')
#file_date='11-19'


printf "***************NCS 7:51 json file*******************\n"
more  ./log/Day2check_info_2020-${file_date}-07-51.log | grep there  | wc -l
printf "\n"

printf "***************admin_dir_disk0_location_all*******************\n"
ls admin_dir_disk0_location_all/*${file_date}*.json  | wc -l 
printf "\n"

printf "***************admin_dir_harddisk_location_all*******************\n"
ls admin_dir_harddisk_location_all/*${file_date}*.json  | wc -l
printf "\n"

printf "***************admin_dir_rootfs_location_all*******************\n" 
ls admin_dir_rootfs_location_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_alarms_brief*******************\n"
ls admin_show_alarms_brief/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_chassis*******************\n"
ls admin_show_chassis/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_controller_fabric_bundle_all_detail*******************\n"
ls admin_show_controller_fabric_bundle_all_detail/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_controller_fabric_link_port_s2_rx_state_down*******************\n"
ls admin_show_controller_fabric_link_port_s2_rx_state_down/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_controller_fabric_link_port_s3_rx_state_down*******************\n"
ls admin_show_controller_fabric_link_port_s3_rx_state_down/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_controller_fabric_plane_all_detail*******************\n"
ls admin_show_controller_fabric_plane_all_detail/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_controller_fabric_plane_all_statistics*******************\n"
ls admin_show_controller_fabric_plane_all_statistics/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_controller_fabric_sfe_fia_all*******************\n"
ls admin_show_controller_fabric_sfe_fia_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_controller_fabric_sfe_s13_all*******************\n"
ls admin_show_controller_fabric_sfe_s13_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_controller_fabric_sfe_s2_all*******************\n"
ls admin_show_controller_fabric_sfe_s2_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_environment_fan_ft*******************\n"
ls admin_show_environment_fan_ft/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_environment_fan_pt*******************\n"
ls admin_show_environment_fan_pt/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_environment_power*******************\n"
ls admin_show_environment_power/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_hw-module_fpd*******************\n"
ls admin_show_hw-module_fpd/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_install_active_summary*******************\n"
ls admin_show_install_active_summary/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_install_inactive_summary*******************\n"
ls admin_show_install_inactive_summary/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_install_superseded_summary*******************\n"
ls admin_show_install_superseded_summary/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_led*******************\n"
ls admin_show_led/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_platform*******************\n"
ls admin_show_platform/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_platform_slice*******************\n"
ls admin_show_platform_slice/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_sdr_default-sdr_pairing*******************\n"
ls admin_show_sdr_default-sdr_pairing/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************admin_show_vm*******************\n"
ls admin_show_vm/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_bgp_neighbors*******************\n"
ls show_bgp_neighbors/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_context_location_all*******************\n"
ls show_context_location_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_gsp_location_00*******************\n"
ls show_health_gsp_location_00/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_gsp_location_01*******************\n"
ls show_health_gsp_location_01/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_gsp_location_10*******************\n"
ls show_health_gsp_location_10/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_gsp_location_11*******************\n"
ls show_health_gsp_location_11/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_gsp_location_20*******************\n"
ls show_health_gsp_location_20/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_gsp_location_21*******************\n"
ls show_health_gsp_location_21/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_sysdb_location_00*******************\n"
ls show_health_sysdb_location_00/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_sysdb_location_01*******************\n"
ls show_health_sysdb_location_01/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_sysdb_location_10*******************\n"
ls show_health_sysdb_location_10/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_sysdb_location_11*******************\n"
ls show_health_sysdb_location_11/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_sysdb_location_20*******************\n"
ls show_health_sysdb_location_20/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_health_sysdb_location_21*******************\n"
ls show_health_sysdb_location_21/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_install_active_summary*******************\n"
ls show_install_active_summary/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_install_inactive_summary*******************\n"
ls show_install_inactive_summary/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_install_superseded_summary*******************\n"
ls show_install_superseded_summary/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_memory_summary_location_all*******************\n"
ls show_memory_summary_location_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_ntp_status*******************\n"
ls show_ntp_status/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_placement_reoptimize*******************\n"
ls show_placement_reoptimize/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_aborts_location_all*******************\n"
ls show_processes_aborts_location_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_blocked_location_all*******************\n"
ls show_processes_blocked_location_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_cpu_location_00*******************\n"
ls show_processes_cpu_location_00/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_cpu_location_01*******************\n"
ls show_processes_cpu_location_01/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_cpu_location_10*******************\n"
ls show_processes_cpu_location_10/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_cpu_location_11*******************\n"
ls show_processes_cpu_location_11/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_cpu_location_20*******************\n"
ls show_processes_cpu_location_20/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_cpu_location_21*******************\n"
ls show_processes_cpu_location_21/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_processes_memory_location_all*******************\n"
ls show_processes_memory_location_all/*${file_date}*.json  | wc -l 
printf "\n"


printf "***************show_redundancy_summary*******************\n"
ls show_redundancy_summary/*${file_date}*.json  | wc -l 
printf "\n"


