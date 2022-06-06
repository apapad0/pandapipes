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

# create loads
pandapipes.create_sinks(net, junctions=sink_junctions, mdot_kg_per_s=mdot, index=[1, 2])



