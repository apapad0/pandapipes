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

# create loads
pandapipes.create_sinks(net, junctions=[1, 2], mdot_kg_per_s=1, index=[1, 2])

# run pipeflow
pandapipes.pipeflow(net, stop_condition="tol", iter=100, friction_model="colebrook",
                    mode="all", transient=False, nonlinear_method="automatic", tol_res=1e-4)

# print(net.res_junction)
# print(net.res_pipe)
# print(net.res_sink)
# net.res_pipe.to_csv("pipes_example.csv")
# net.res_junction.to_csv("junctions_example.csv")
