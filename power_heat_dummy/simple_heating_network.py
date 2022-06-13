import pandapipes

# create empty network
net = pandapipes.create_empty_network(fluid="water", name="Simple meshed district heating network")

# create junctions
pandapipes.create_junctions(net, nr_junctions=3, pn_bar=3, tfluid_k=[323.15, 323.15, 373.15], index=[1, 2, 3])

# create external grid
pandapipes.create_ext_grid(net, junction=3, p_bar=6, t_k=373.15, name="Source")

# create pipes
pandapipes.create_pipes_from_parameters(net, from_junctions=[3, 1, 3], to_junctions=[1, 2, 2], length_km=[0.4, 0.4, 0.6],
                                        diameter_m=0.15, k_mm=1.25, sections=1, alpha_w_per_m2k=0.2, index=[1, 2, 3])

sink_junctions = [1, 2]
sink_p_mwth = [0.3, 0.3]
t_source = net["ext_grid"]["t_k"][0]
t_load = [net["junction"]["tfluid_k"][junction] for junction in sink_junctions]
mdot = [mwth / (4.182 * 0.001 * (t_source - t_load[index])) for index, mwth in enumerate(sink_p_mwth)]

mwel = 0.15
cop = 4
mdot_source = mwel * cop / (4.182 * 0.001 * 50)


# create loads
pandapipes.create_sinks(net, junctions=sink_junctions, mdot_kg_per_s=mdot, index=[1, 2])
# create source
# pandapipes.create_source(net, junction=1, mdot_kg_per_s=mdot_source, index=1)

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
# pandapipes.pipeflow(net=net, **pipeflow_attributes)
#
# print(net['res_junction'])
# print(net['res_pipe']['mdot_from_kg_per_s'])



