from netmiko import ConnectHandler
import yaml


Routers = {"R1": {"device_type": "nokia_srl", "host": "172.20.20.2", "username": "admin", "password": "NokiaSrl1!"},
           "R2" : {"device_type": "nokia_srl", "host": "172.20.20.3", "username": "admin", "password": "NokiaSrl1!"}
           }            # Dictionnary of Routers 


R1 = {
    "device_type": "nokia_srl",
    "host": "172.20.20.2",
    "username": "admin",
    "password": "NokiaSrl1!"
   
}


R2 = {
    "device_type": "nokia_srl",
    "host": "172.20.20.2",
    "username": "admin",
    "password": "NokiaSrl1!"
   
}





Path = "d:/Network Automation/yamlfile.yml"   #This is the path of the yaml file

 
with open(Path, 'r') as stream:
    try:
        parsed_yaml=yaml.safe_load(stream)
        devices= parsed_yaml["endpoints"]  # Retrieve the endpoints of the VRF from the Yaml file
        vrf_name= parsed_yaml["vrf name"] # Retrieve the VRF Name from the Yaml file
        desc_vrf= parsed_yaml["description"] # Retrieve the VRF Description from the Yaml file
        route_distinguisher=parsed_yaml["route distinguisher"] # Retrieve the route distinguisher from the yaml
        route_target=parsed_yaml["route target"] # Retrieve the route target from the yaml
       
       
         #
         #
     


     
    except yaml.YAMLError as exc:
        print(exc)


        

for dev in devices :                           
    
    
    connection_router = Routers[dev] 
    
    connection = ConnectHandler(**connection_router)
    connection.enable()

    print (f" --------------STARTING CONFIGURATION ON {dev} ---------------------------" )
       
    enter_candidate = "enter candidate"
    config_vrf = f"set /network-instance {vrf_name} type ip-vrf"
    
    congig_desc_vrf = f"set /network-instance {vrf_name} description {desc_vrf}"

    config_route_target_export = f"set /network-instance {vrf_name} protocols bgp-vpn bgp-instance 1 route-target export-rt target:{route_target}"
    config_route_target_import = f"set /network-instance {vrf_name} protocols bgp-vpn bgp-instance 1 route-target import-rt target:{route_target}"
    config_route_distinguisher = f"set /network-instance {vrf_name} protocols bgp-vpn bgp-instance 1 route-distinguisher rd {route_distinguisher}"

    config_route_dis = f"set /network-instance {vrf_name}  {route_distinguisher}"

    commands= ['enter candidate', config_vrf, congig_desc_vrf,config_route_distinguisher, config_route_target_import,config_route_target_export]

    output = connection.send_config_set(commands)
    print(output)



    for intf in parsed_yaml["interfaces"][dev] :       # Search the interfaces from the Yaml file

        

        port_id = intf["port id"]
        ip_address = intf["ip address"]
        subnet_mask = intf["subnet mask"]
        description = intf["description"]
        
        config_id = f"set /interface {port_id} admin-state enable"
        config_desc = f"set /interface {port_id} description {description}" 
        config_ip = f"set /interface {port_id} subinterface 0 ipv4 address {ip_address}/{subnet_mask}"
        assign_ip_vrf = f" set /network-instance {vrf_name} interface {port_id} "

        
        commands= ['enter candidate', config_id,config_desc, config_ip,assign_ip_vrf]

        output = connection.send_config_set(commands)
        print(output)


    print('Closing Connection')

    print (f" --------------END OF CONFIGURATION ON {dev} ---------------------------" )
    connection.disconnect()
