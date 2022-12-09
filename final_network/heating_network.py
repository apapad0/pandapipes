import math
import os

import pandapipes

# create empty network
net = pandapipes.create_empty_network(fluid="water")

# create junctions
pandapipes.create_junctions(net, nr_junctions=64, pn_bar=18, tfluid_k=378.15, index=[i for i in range(1, 65)])

# create external grid
pandapipes.create_ext_grid(net, junction=1, p_bar=18, t_k=378.15, name="External grid")

# pipes properties
from_junction = [1, 2, 2, 4, 4, 6, 6, 8, 8, 10, 10, 12, 12, 14, 14, 16, 16, 18, 18, 20, 20, 22, 23, 23, 25, 25, 27, 27,
                 29, 29, 31, 22, 33, 33, 35, 36, 36, 38, 38, 40, 40, 42, 42, 44, 45, 45, 47, 44, 49, 49, 51, 51, 53, 53,
                 55, 55, 57, 57, 59, 59, 61, 61, 63]
pipe_length_m = [4.8569, 6.7268, 4.906, 10.1672, 9.0815, 4.4881, 12.0975, 7.5329, 6.4219, 7.5968, 6.3183, 4.8686,
                 9.4594, 4.4605, 2.9831, 10.5656, 2.7041, 9.5488, 6.2788, 4.0524, 11.2925, 28.5724, 6.1725, 21.0723,
                 4.7574, 8.0382, 9.7141, 14.6253, 7.8439, 18.8285, 9.1868, 3.0376, 11.2216, 10.2214, 18.9767, 12.4134,
                 6.2911, 5.2326, 3.6398, 9.9703, 8.3603, 10.5488, 18.1950, 23.2380, 23.5073, 9.0411, 3.9901, 9.1700,
                 15.2297, 3.8622, 9.4209, 21.3474, 12.1829, 4.7677, 6.3136, 5.2862, 29.2504, 16.2316, 6.6540, 14.5921,
                 3.5921, 10.1751, 4.5408]
pipe_diameter_mm = [125, 25, 125, 40, 125, 25, 125, 25, 125, 25, 125, 25, 125, 25, 125, 25, 125, 25, 125, 25, 125, 50,
                    32, 50, 25, 50, 25, 50, 25, 50, 25, 125, 25, 125, 65, 25, 65, 25, 65, 32, 65, 25, 65, 40, 32, 40,
                    25, 65, 25, 65, 25, 65, 25, 65, 25, 65, 25, 65, 25, 65, 25, 65, 25]
pipe_diameter_m = [x/1000 for x in pipe_diameter_mm]

# create pipes
pandapipes.create_pipes_from_parameters(net, from_junctions=from_junction, to_junctions=[i for i in range(2, 65)],
                                        length_km=[element/1000 for element in pipe_length_m],
                                        diameter_m=pipe_diameter_m, k_mm=0.045, sections=1,
                                        alpha_w_per_m2k=[0.027/(math.pi*d) for d in pipe_diameter_m], text_k=283.15)

# load properties
sink_junction = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 24, 26, 28, 30, 32, 34, 37, 39, 41, 43, 46, 48, 50, 52, 54, 56,
                 58, 60, 62, 64]
load_mcal_h = [40, 100, 40, 40, 40, 40, 40, 40, 20, 40, 60, 20, 40, 40, 40, 40, 40, 40, 60, 40, 40, 40, 40, 40, 40, 40,
               40, 40, 40, 40]
t_load = [net["junction"]["tfluid_k"][junction] for junction in sink_junction]
mdot = [cal * 0.001162 / (4.182 * 0.001 * (t_load[index] - 348.15)) for index, cal in enumerate(load_mcal_h)]

# create loads
pandapipes.create_sinks(net, junctions=sink_junction, mdot_kg_per_s=mdot)


pipeflow_attributes = {
    "stop_condition": "tol",
    "iter": 100,
    "friction_model": "colebrook",
    "mode": "all",
    "transient": False,
    "nonlinear_method": "automatic",
    "tol_res": 1e-4
}

# run pipeflow
if __name__ == "__main__":
    pandapipes.pipeflow(net=net, **pipeflow_attributes)
    os.makedirs("csv_files", exist_ok=True)
    print(net['res_junction'])
    print(net['res_pipe']['mdot_from_kg_per_s'])

    net.res_junction.to_csv("csv_files/junction_pressure_temperature.csv")
    net.res_pipe.mdot_from_kg_per_s.to_csv("csv_files/pipes_mdot.csv")
