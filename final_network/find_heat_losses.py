import copy
import csv
import os

import pandapower

import pandapipes
from electricity_network import net as net_power
from heating_network import net as net_heat
from pandapipes.multinet.control.controller.multinet_control import P2HControlMultiEnergy
from pandapipes.multinet.control.run_control_multinet import run_control
from pandapipes.multinet.create_multinet import create_empty_multinet, add_net_to_multinet
from pandapipes.pipeflow import PipeflowNotConverged

BRANCH_1 = [i for i in [24, 28, 30, 32]]
BRANCH_2 = [i for i in [34, 37, 39, 41, 43, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64]]

COP = 2
CP = 4.182 * 0.001

load1 = 35 * 0.001162 / COP
load2 = 95 * 0.001162 / COP
load3 = 35 * 0.001162 / COP


def create_multinet(power_net, heat_net, junction, bus=[5, 17, 19]):
    multinet = create_empty_multinet('power_heat_multinet')
    # Add networks to multinet
    add_net_to_multinet(multinet, power_net, 'power')
    add_net_to_multinet(multinet, heat_net, 'heat')

    # create elements corresponding to conversion units:
    # connection 1
    p2h_id_el_1 = pandapower.create_load(power_net, bus=bus[0], p_mw=load1, name="power to heat consumption 1")
    p2h_id_heat_1 = pandapipes.create_source(heat_net, junction=junction[0], mdot_kg_per_s=0,
                                             name="power to heat feed in 1 ")
    # connection 2
    p2h_id_el_2 = pandapower.create_load(power_net, bus=bus[1], p_mw=load2, name="power to heat consumption 2")
    p2h_id_heat_2 = pandapipes.create_source(heat_net, junction=junction[1], mdot_kg_per_s=0,
                                             name="power to heat feed in 2")
    # connection 3
    p2h_id_el_3 = pandapower.create_load(power_net, bus=bus[2], p_mw=load3, name="power to heat consumption 3")
    p2h_id_heat_3 = pandapipes.create_source(heat_net, junction=junction[2], mdot_kg_per_s=0,
                                             name="power to heat feed in 3")

    # create coupling controllers:
    P2HControlMultiEnergy(multinet, p2h_id_el_1, p2h_id_heat_1, cop_factor=COP, in_temp=348.15, out_temp=383.15,
                          name_power_net="power", name_heat_net="heat")

    P2HControlMultiEnergy(multinet, p2h_id_el_2, p2h_id_heat_2, cop_factor=COP, in_temp=348.15, out_temp=383.15,
                          name_power_net="power", name_heat_net="heat")

    P2HControlMultiEnergy(multinet, p2h_id_el_3, p2h_id_heat_3, cop_factor=COP, in_temp=348.15, out_temp=383.15,
                          name_power_net="power", name_heat_net="heat")
    return multinet


def create_csv(file_name, data):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['junctions', 'losses']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow({'junctions': item['junctions'], 'losses': item['losses']})


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
    losses = []
    for connection_1 in BRANCH_1:
        for connection_2 in BRANCH_2:
            power_net_copy = copy.deepcopy(net_power)
            heat_net_copy = copy.deepcopy(net_heat)
            multinet = create_multinet(power_net=power_net_copy, heat_net=heat_net_copy,
                                       junction=[connection_1, 5, connection_2])
            try:
                run_control(multinet, **pipeflow_attributes)
            except PipeflowNotConverged:
                continue
            pipe_losses = 0
            for index, row in multinet['nets']['heat']['res_pipe'].iterrows():
                pipe_losses += CP * row['mdot_from_kg_per_s'] * (row['t_from_k'] - row['t_to_k'])
            losses.append({"junctions": f"{connection_1}_5_{connection_2}", "losses": pipe_losses})

    os.makedirs("csv_files", exist_ok=True)
    create_csv(file_name="csv_files/losses_analysis.csv", data=losses)
