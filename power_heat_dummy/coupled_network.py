import pandapower
import pandapipes

from power_flow_combined import net as net_power
from simple_heating_network import net as net_heat

from pandapipes.multinet.create_multinet import create_empty_multinet, add_net_to_multinet
from pandapipes.multinet.control.run_control_multinet import run_control

from pandapipes.multinet.control.controller.multinet_control import P2HControlMultiEnergy, H2PControlMultiEnergy


# create multinet and add networks:
multinet = create_empty_multinet('power_heat_multinet')
add_net_to_multinet(multinet, net_power, 'power')
add_net_to_multinet(multinet, net_heat, 'heat')


# create elements corresponding to conversion units:
p2h_id_el = pandapower.create_load(net_power, bus=8, p_mw=0.07, name="power to heat consumption")
p2h_id_heat = pandapipes.create_source(net_heat, junction=1, mdot_kg_per_s=0, name="power to heat feed in")

h2p_id_heat = pandapipes.create_sink(net_heat, junction=1, mdot_kg_per_s=0, name="heat to power consumption")
h2p_id_el = pandapower.create_sgen(net_power, bus=8, p_mw=0, name="fuel cell feed in")


# create coupling controllers:
p2h_ctrl = P2HControlMultiEnergy(multinet, p2h_id_el, p2h_id_heat, cop_factor=4, out_temp=373.15,
                                 name_power_net="power", name_heat_net="heat")

# h2p_ctrl = H2PControlMultiEnergy(multinet, h2p_id_el, h2p_id_heat, h2p_ratio=1.3, temp_diff=30,
#                                  name_power_net="power", name_heat_net="heat")

# run simulation:
run_control(multinet)

print(net_heat.source.loc[p2h_id_heat, 'mdot_kg_per_s'])
# print(net_power.sgen.loc[h2p_id_el, 'p_mw'])

buses = list([i for i in range(1, 7)]) + [8, 9]
for bus in buses:
    print(str(net_power.bus.name[bus]) + ': ' + str(round(net_power.res_bus.vm_pu[bus], 7)))

print(net_heat.res_junction["t_k"])
print(net_heat.res_pipe)
# net_heat.res_pipe.to_csv("pipes_example.csv")
