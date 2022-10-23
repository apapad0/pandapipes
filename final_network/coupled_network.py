import pandapower
import os

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
cop = 2

load1 = 35 * 0.001162 / cop
load2 = 95 * 0.001162 / cop
load3 = 35 * 0.001162 / cop

# create elements corresponding to conversion units:
# connection 1
p2h_id_el_1 = pandapower.create_load(net_power, bus=5, p_mw=load1, name="power to heat consumption 1")
p2h_id_heat_1 = pandapipes.create_source(net_heat, junction=32, mdot_kg_per_s=0, name="power to heat feed in 1 ")
# connection 2
p2h_id_el_2 = pandapower.create_load(net_power, bus=17, p_mw=load2, name="power to heat consumption 2")
p2h_id_heat_2 = pandapipes.create_source(net_heat, junction=5, mdot_kg_per_s=0, name="power to heat feed in 2")
# connection 3
p2h_id_el_3 = pandapower.create_load(net_power, bus=19, p_mw=load3, name="power to heat consumption 3")
p2h_id_heat_3 = pandapipes.create_source(net_heat, junction=64, mdot_kg_per_s=0, name="power to heat feed in 3")

# create coupling controllers:
p2h_ctrl_1 = P2HControlMultiEnergy(multinet, p2h_id_el_1, p2h_id_heat_1, cop_factor=cop, out_temp=368.15,
                                   name_power_net="power", name_heat_net="heat")

p2h_ctrl_2 = P2HControlMultiEnergy(multinet, p2h_id_el_2, p2h_id_heat_2, cop_factor=cop, out_temp=368.15,
                                   name_power_net="power", name_heat_net="heat")

p2h_ctrl_3 = P2HControlMultiEnergy(multinet, p2h_id_el_3, p2h_id_heat_3, cop_factor=cop, out_temp=368.15,
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
if __name__ == "__main__":
    run_control(multinet, **pipeflow_attributes)
    os.makedirs("csv_files", exist_ok=True)

    print(multinet['nets']['power']['res_bus']['vm_pu'])
    print(multinet['nets']['heat']['res_junction'])

    print("PASS" if all(0.9 < multinet['nets']['power']['res_bus']['vm_pu'][index] < 1.1 for index in range(1, 27))
          else "FAIL")
    print(multinet['nets']['heat']['res_pipe']['mdot_from_kg_per_s'])
    print(multinet['nets']['power']['res_ext_grid']['p_mw'])

    multinet['nets']['power']['res_bus']['vm_pu'].to_csv("csv_files/bus_voltage.csv")
    multinet['nets']['heat']['res_junction']['t_k'].to_csv("csv_files/temperature.csv")