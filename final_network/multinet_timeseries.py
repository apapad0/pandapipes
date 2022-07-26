from os.path import join, dirname

import pandapower
import pandas
from pandapower.timeseries import DFData, OutputWriter

import pandapipes
from coupled_network import multinet, p2h_id_el_1, p2h_id_heat_1, p2h_id_el_2, p2h_id_heat_2, pipeflow_attributes
from pandapipes.multinet.timeseries.run_time_series_multinet import run_timeseries
from pandapipes.multinet.control.controller.multinet_control import coupled_p2h_const_control


def create_datasource(csv_name):
    df = pandas.read_csv(csv_name)
    ds = DFData(df)
    return ds


def create_output_writers(multinet, time_steps=None):
    nets = multinet["nets"]
    ows = dict()
    for key_net in nets.keys():
        ows[key_net] = {}
        if isinstance(nets[key_net], pandapower.pandapowerNet):
            log_variables = [('res_bus', 'vm_pu'),
                             ('res_line', 'loading_percent'),
                             ('res_line', 'i_ka'),
                             ('res_bus', 'p_mw'),
                             ('res_bus', 'q_mvar'),
                             ('res_load', 'p_mw'),
                             ('res_load', 'q_mvar')]
            ow = OutputWriter(nets[key_net], time_steps=time_steps,
                              log_variables=log_variables,
                              output_path=join(dirname('__file__'), 'timeseries', 'results', 'power'),
                              output_file_type=".csv", csv_separator=",")
            ows[key_net] = ow
        elif isinstance(nets[key_net], pandapipes.pandapipesNet):
            log_variables = [('res_sink', 'mdot_kg_per_s'),
                             ('res_source', 'mdot_kg_per_s'),
                             ('res_ext_grid', 'mdot_kg_per_s'),
                             ('res_pipe', 'v_mean_m_per_s'),
                             ('res_junction', 'p_bar'),
                             ('res_junction', 't_k')]
            ow = OutputWriter(nets[key_net], time_steps=time_steps,
                              log_variables=log_variables,
                              output_path=join(dirname('__file__'), 'timeseries', 'results', 'heat'),
                              output_file_type=".csv", csv_separator=",")
            ows[key_net] = ow
        else:
            raise AttributeError("Could not create an output writer for nets of kind " + str(key_net))
    return ows


if __name__ == "__main__":
    timesteps = range(8)
    ds = create_datasource("loads.csv")
    ows = create_output_writers(multinet, timesteps)
    coupled_p2h_const_control(multinet, p2h_id_el_1, p2h_id_heat_1, cop_factor=4, out_temp=378.15,
                              name_power_net="power", name_heat_net="heat", profile_name=["load_1"], data_source=ds)
    coupled_p2h_const_control(multinet, p2h_id_el_2, p2h_id_heat_2, cop_factor=4, out_temp=378.15,
                              name_power_net="power", name_heat_net="heat", profile_name=["load_2"], data_source=ds)

    run_timeseries(multinet, time_steps=timesteps, output_writers=ows, **pipeflow_attributes)