import pandapower

# create empty network
net = pandapower.create_empty_network()

# create buses
pandapower.create_buses(net, nr_buses=8, vn_kv=[11., 11., 11., 11., 11., 11., 11., 33.], name=list(['Bus ' + str(i) for i in range(1, 7)] + ['Bus 8', 'Bus 9']), index=list([i for i in range(1, 7)]) + [8, 9])

# create Slack bus
pandapower.create_ext_grid(net, bus=9, vm_pu=1.02, va_degree=0, name='Slackbus', in_service=True)

# create transformer
pandapower.create_transformer_from_parameters(net, hv_bus=9, lv_bus=2, sn_mva=15, vn_hv_kv=33, vn_lv_kv=11, vkr_percent=1.197, pfe_kw=0, i0_percent=0, vk_percent=18, vector_group='Yyn', name="Head Transformer")

# cable properties
r_ohm = 0.164
x_ohm = 0.080
c_nf = 0
max_i = 0.498

# create cables
pandapower.create_lines_from_parameters(net, from_buses=[2, 2, 3, 8, 8, 5], to_buses=[1, 3, 4, 4, 5, 6], length_km=[0.26, 0.17, 0.23, 0.32, 0.20, 0.16], r_ohm_per_km=r_ohm, x_ohm_per_km=x_ohm, c_nf_per_km=c_nf, max_i_ka=max_i, index=[i for i in range(1, 7)])

# create loads
pandapower.create_loads(net, buses=[1, 3, 4, 5, 6], p_mw=[0.2, 0.5, 0.5, 0.2, 0.2], q_mvar=0, index=[i for i in range(1, 6)])


# run powerflow
pandapower.runpp(net)

# # print voltage per bus
# for index in range(1, 7):
#     print(str(net.bus.name[index]) + ': ' + str(round(net.res_bus.vm_pu[index], 7)))
# print(str(net.bus.name[8]) + ': ' + str(round(net.res_bus.vm_pu[8], 7)))
# print(str(net.bus.name[9]) + ': ' + str(round(net.res_bus.vm_pu[9], 7)))

