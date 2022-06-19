import pandapower

import pandapipes
from pandapipes.multinet.control.controller.multinet_control import P2HControlMultiEnergy
from pandapipes.multinet.control.run_control_multinet import run_control
from pandapipes.multinet.create_multinet import create_empty_multinet, add_net_to_multinet
from power_flow_combined import net as net_power
from simple_heating_network import net as net_heat

# create multinet and add networks:
multinet = create_empty_multinet('power_heat_multinet')
add_net_to_multinet(multinet, net_power, 'power')
add_net_to_multinet(multinet, net_heat, 'heat')


# create elements corresponding to conversion units:
p2h_id_el = pandapower.create_load(net_power, bus=8, p_mw=0.15, name="power to heat consumption")
p2h_id_heat = pandapipes.create_source(net_heat, junction=1, mdot_kg_per_s=0, name="power to heat feed in")


# create coupling controllers:
# p2h_ctrl = P2HControlMultiEnergy(multinet, p2h_id_el, p2h_id_heat, cop_factor=4, out_temp=373.15,
#                                  name_power_net="power", name_heat_net="heat")

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
# run_control(multinet, **pipeflow_attributes)
#
# print(net_heat.source.loc[p2h_id_heat, 'mdot_kg_per_s'])
#
# print(multinet['nets']['power']['res_bus']['vm_pu'])
# print(multinet['nets']['heat']['res_junction'])
# print(multinet['nets']['heat']['res_pipe']['mdot_from_kg_per_s'])
# print(multinet['nets']['power']['res_ext_grid']['p_mw'])
