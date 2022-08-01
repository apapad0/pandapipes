import pandapower

import pandapipes
from pandapipes.multinet.control.controller.multinet_control import P2HControlMultiEnergy
from pandapipes.multinet.control.run_control_multinet import run_control
from pandapipes.multinet.create_multinet import create_empty_multinet, add_net_to_multinet
from electricity_network import net as net_power
from heating_network import net as net_heat

# create multinet and add networks:
multinet = create_empty_multinet('power_heat_multinet')
add_net_to_multinet(multinet, net_power, 'power')
add_net_to_multinet(multinet, net_heat, 'heat')

load1 = 50 * 0.001162 / 4
load2 = 40 * 0.001162 / 4

# create elements corresponding to conversion units:
# connection 1
p2h_id_el_1 = pandapower.create_load(net_power, bus=11, p_mw=load1, name="power to heat consumption 1")
p2h_id_heat_1 = pandapipes.create_source(net_heat, junction=5, mdot_kg_per_s=0, name="power to heat feed in 1 ")
# connection 2
p2h_id_el_2 = pandapower.create_load(net_power, bus=18, p_mw=load2, name="power to heat consumption 2")
p2h_id_heat_2 = pandapipes.create_source(net_heat, junction=64, mdot_kg_per_s=0, name="power to heat feed in 2")

# create coupling controllers:
p2h_ctrl_1 = P2HControlMultiEnergy(multinet, p2h_id_el_1, p2h_id_heat_1, cop_factor=4, out_temp=378.15,
                                   name_power_net="power", name_heat_net="heat")

p2h_ctrl_2 = P2HControlMultiEnergy(multinet, p2h_id_el_2, p2h_id_heat_2, cop_factor=4, out_temp=378.15,
                                   name_power_net="power", name_heat_net="heat")

pipeflow_attributes = {
    "stop_condition": "tol",
    "iter": 100,
    "friction_model": "colebrook",
    "mode": "all",
    "transient": False,
    "nonlinear_method": "automatic",
    "tol_res": 1e-4
}

# # run simulation:
run_control(multinet, **pipeflow_attributes)
#
print(multinet['nets']['power']['res_bus']['vm_pu'])
print(multinet['nets']['heat']['res_junction'])
# print(multinet['nets']['heat']['res_pipe']['mdot_from_kg_per_s'])
# print(multinet['nets']['power']['res_ext_grid']['p_mw'])
