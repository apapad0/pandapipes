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
p2h_id_el = pandapower.create_load(net_power, bus=8, p_mw=0.07, name="power to heat consumption")
p2h_id_heat = pandapipes.create_source(net_heat, junction=1, mdot_kg_per_s=0, name="power to heat feed in")


# create coupling controllers:
p2h_ctrl = P2HControlMultiEnergy(multinet, p2h_id_el, p2h_id_heat, cop_factor=4, out_temp=373.15,
                                 name_power_net="power", name_heat_net="heat")

control_variables = {
    "run": 'net=net_heat, stop_condition="tol", iter=100, friction_model="colebrook", mode="all", transient=False, nonlinear_method="automatic", tol_res=1e-4)'
}


# run simulation:
run_control(multinet, ctrl_variables=control_variables)

print(net_heat.source.loc[p2h_id_heat, 'mdot_kg_per_s'])

buses = list([i for i in range(1, 7)]) + [8, 9]
for bus in buses:
    print(str(net_power.bus.name[bus]) + ': ' + str(round(net_power.res_bus.vm_pu[bus], 7)))

print(net_heat.res_junction["t_k"])
# net_heat.res_pipe.to_csv("pipes_example.csv")
