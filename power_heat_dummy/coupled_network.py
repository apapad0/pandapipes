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
p2h_id_el = pandapower.create_load(net_power, bus=8, p_mw=0.3, name="power to heat consumption")
p2h_id_heat = pandapipes.create_source(net_heat, junction=1, mdot_kg_per_s=1, name="power to gas feed in")

h2p_id_heat = pandapipes.create_sink(net_heat, junction=1, mdot_kg_per_s=1, name="gas to power consumption")
h2p_id_el = pandapower.create_sgen(net_power, bus=8, p_mw=0.5, name="fuel cell feed in")


# create coupling controllers:
p2h_ctrl = P2HControlMultiEnergy(multinet, p2h_id_el, p2h_id_heat, efficiency=1,
                                 name_power_net="power", name_gas_net="heat")

h2p_ctrl = H2PControlMultiEnergy(multinet, h2p_id_el, h2p_id_heat, efficiency=1,
                                 name_power_net="power", name_gas_net="heat")

# run simulation:
run_control(multinet)

print(net_heat.source.loc[p2h_id_heat, 'mdot_kg_per_s'])
print(net_power.sgen.loc[h2p_id_el, 'p_mw'])