import pandapower

# create empty network
net = pandapower.create_empty_network()

# create buses
pandapower.create_buses(net, nr_buses=26, vn_kv=list([20.] + [0.4 for i in range(25)]),
                        index=list([i for i in range(1, 27)]))

# create Feeder
pandapower.create_ext_grid(net, bus=1, vm_pu=1., va_degree=0, name='Feeder', in_service=True)


# create transformer
pandapower.create_transformer_from_parameters(net, hv_bus=1, lv_bus=2, sn_mva=0.25, vn_hv_kv=20., vn_lv_kv=0.4,
                                              vkr_percent=1.3, pfe_kw=0, i0_percent=0, vk_percent=4,
                                              vector_group='Yy0', name="Transformer")

# backbone line properties
r_ohm1 = 0.6538
x_ohm1 = 0.0769
c_nf1 = 0
max_i1 = 0.145

# branch line properties
r_ohm2 = 0.9393
x_ohm2 = 0.0909
c_nf2 = 0
max_i2 = 0.120


# create backbone lines
pandapower.create_lines_from_parameters(net, from_buses=[2, 3, 4, 5, 6, 12, 13, 14, 18],
                                        to_buses=[3, 4, 5, 6, 12, 13, 14, 18, 19],
                                        length_km=[0.050, 0.100, 0.075, 0.025, 0.075, 0.040, 0.050, 0.040, 0.050],
                                        r_ohm_per_km=r_ohm1, x_ohm_per_km=x_ohm1, c_nf_per_km=c_nf1, max_i_ka=max_i1,
                                        index=[2, 3, 4, 5, 11, 12, 13, 17, 18])
# create branch1 lines
pandapower.create_lines_from_parameters(net, from_buses=[6, 7, 8, 9, 10], to_buses=[7, 8, 9, 10, 11],
                                        length_km=[0.025, 0.050, 0.025, 0.050, 0.075],
                                        r_ohm_per_km=r_ohm2, x_ohm_per_km=x_ohm2, c_nf_per_km=c_nf2, max_i_ka=max_i2,
                                        index=[6, 7, 8, 9, 10])
# create branch2 lines
pandapower.create_lines_from_parameters(net, from_buses=[14, 15, 16], to_buses=[15, 16, 17],
                                        length_km=[0.050, 0.025, 0.050],
                                        r_ohm_per_km=r_ohm2, x_ohm_per_km=x_ohm2, c_nf_per_km=c_nf2, max_i_ka=max_i2,
                                        index=[14, 15, 16])
# create branch3 lines
pandapower.create_lines_from_parameters(net, from_buses=[6, 20, 21, 22], to_buses=[20, 21, 22, 23],
                                        length_km=[0.025, 0.050, 0.075, 0.050],
                                        r_ohm_per_km=r_ohm2, x_ohm_per_km=x_ohm2, c_nf_per_km=c_nf2, max_i_ka=max_i2,
                                        index=[19, 20, 21, 22])
# create branch4 lines
pandapower.create_lines_from_parameters(net, from_buses=[5, 24, 25], to_buses=[24, 25, 26],
                                        length_km=[0.050, 0.075, 0.050],
                                        r_ohm_per_km=r_ohm2, x_ohm_per_km=x_ohm2, c_nf_per_km=c_nf2, max_i_ka=max_i2,
                                        index=[23, 24, 25])

load_buses = [3, 4, 6, 7, 8, 10, 15, 16, 19, 20, 21, 23, 24, 26]
load_p_mw = [0.005, 0.0075, 0.0125, 0.005, 0.0075, 0.010, 0.005, 0.010, 0.0075, 0.0075, 0.0075, 0.010, 0.0025, 0.0025]
cosphi = 0.95
# create loads
for i in range(len(load_buses)):
    pandapower.create_load_from_cosphi(net, bus=load_buses[i], sn_mva=load_p_mw[i]/cosphi, cos_phi=cosphi,
                                       mode="underexcited", index=load_buses[i])

# create sgen
pandapower.create_sgens(net, buses=[5, 9, 11, 12, 13, 14, 17, 18, 22, 25],
                        p_mw=[0.015, 0.020, 0.015, 0.015, 0.015, 0.010, 0.025, 0.030, 0.025, 0.025])

# run powerflow
pandapower.runpp(net)

print(net['res_bus']['vm_pu'])
print(net['res_ext_grid']['p_mw'])

net.res_bus.vm_pu.to_csv("bus_voltage.csv")