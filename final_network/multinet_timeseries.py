from os.path import join, dirname

import pandapower
import pandas
from pandapower.timeseries import DFData, OutputWriter

import pandapipes
from coupled_network import multinet, p2h_id_el_1, p2h_id_heat_1, p2h_id_el_2, p2h_id_heat_2, p2h_id_el_3, \
    p2h_id_heat_3, pipeflow_attributes
from pandapipes.multinet.control.controller.multinet_control import coupled_p2h_const_control
from pandapipes.multinet.timeseries.run_time_series_multinet import run_timeseries
from temperature_celsius import temp_to_celsius


def create_datasource(excel_file):
    df = pandas.read_excel(excel_file)
    return DFData(df)


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
                              output_path=join(dirname('__file__'), 'timeseries', f'cop_{cop}', 'power'),
                              output_file_type=".xlsx")
            ows[key_net] = ow
        elif isinstance(nets[key_net], pandapipes.pandapipesNet):
            log_variables = [('res_pipe', 'mdot_from_kg_per_s'),
                             ('res_junction', 'p_bar'),
                             ('res_junction', 't_k')]
            ow = OutputWriter(nets[key_net], time_steps=time_steps,
                              log_variables=log_variables,
                              output_path=join(dirname('__file__'), 'timeseries', f'cop_{cop}', 'heat'),
                              output_file_type=".xlsx")
            ows[key_net] = ow
        else:
            raise AttributeError("Could not create an output writer for nets of kind " + str(key_net))
    return ows


if __name__ == "__main__":
    timesteps = range(45)
    ds = create_datasource(excel_file="loads.xlsx")
    cops = [2.5, 3.5]
    in_temp = 348.15
    out_temp = 383.15
    for cop in cops:
        ows = create_output_writers(multinet, timesteps)
        coupled_p2h_const_control(multinet, p2h_id_el_1, p2h_id_heat_1, cop_factor=cop, in_temp=in_temp,
                                  out_temp=out_temp, name_power_net="power", name_heat_net="heat",
                                  profile_name=[f"load1_cop{cop}"], data_source=ds)
        coupled_p2h_const_control(multinet, p2h_id_el_2, p2h_id_heat_2, cop_factor=cop, in_temp=in_temp,
                                  out_temp=out_temp, name_power_net="power", name_heat_net="heat",
                                  profile_name=[f"load2_cop{cop}"], data_source=ds)
        coupled_p2h_const_control(multinet, p2h_id_el_3, p2h_id_heat_3, cop_factor=cop, in_temp=in_temp,
                                  out_temp=out_temp, name_power_net="power", name_heat_net="heat",
                                  profile_name=[f"load3_cop{cop}"], data_source=ds)
        run_timeseries(multinet, time_steps=timesteps, output_writers=ows, **pipeflow_attributes)
        temp_to_celsius(path=f"timeseries/cop_{cop}/heat/res_junction/t_k")
