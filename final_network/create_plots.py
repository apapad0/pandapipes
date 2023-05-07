import pandapower.plotting as plot
import matplotlib.pyplot as plt
import numpy as np
from pandas import Series


def simple_plot(net):
    # plot Network with loads and sgens
    plot.simple_plot(net, ext_grid_size=3, trafo_size=3, trafo_color="k", plot_loads=True,
                     plot_sgens=True, load_size=1.5, sgen_size=1.5, bus_color='blue')


def simple_plotly(net):
    # Load and sgen details on hover
    plot.simple_plotly(net)


def res_colored_plot(net):
    # Result bus voltages in color
    plot.pf_res_plotly(net)


def collections_figure(net):
    plot.create_generic_coordinates(net)

    buses = net.bus.index.tolist()
    coords = zip(net.bus_geodata.x.loc[buses].values - 0.05, net.bus_geodata.y.loc[buses].values + 0.15)
    bic = plot.create_annotation_collection(size=0.15, texts=np.char.mod('%d', buses), coords=coords, zorder=3,
                                            color='black')
    bc = plot.create_bus_collection(net, buses=net.bus.index, color="black", size=0.1, zorder=2)
    load_buses = [3, 4, 6, 7, 8, 10, 15, 16, 19, 20, 21, 23, 24, 26]

    bc_load = plot.create_bus_collection(net, buses=load_buses, color="red", size=0.1, zorder=3)
    sgen_buses = [5, 9, 11, 12, 13, 14, 17, 18, 22, 25]
    bc_sgen = plot.create_bus_collection(net, buses=sgen_buses, color="green", size=0.1, zorder=3)

    load_gen_buses = [19, 23, 26]
    bc_load_gen = plot.create_bus_collection(net, buses=load_gen_buses, color="brown", size=0.1, zorder=3)

    lc = plot.create_line_collection(net, lines=net.line.index, color="grey", zorder=1)
    tc = plot.create_trafo_collection(net, trafos=net.trafo.index, zorder=1)
    sc = plot.create_bus_collection(net, net.ext_grid.bus.values, patch_type="rect", size=0.12, color="y",
                                    zorder=11)
    plot.draw_collections([bc, lc, tc, sc, bic, bc_load, bc_sgen, bc_load_gen])
    plt.show()


def trace_figure(net):
    plot.create_generic_coordinates(net)
    # lines' trace
    lt = plot.plotly.create_line_trace(net, net.line.index, color='black')
    # buses' trace
    bt = plot.plotly.create_bus_trace(net, net.bus.index, size=10, color="blue", infofunc=Series(index=net.bus.index,
                                      data=net.bus.name + '<br>' + net.bus.vn_kv.astype(str) + ' kV'))
    # transformer's trace
    tt = plot.plotly.create_trafo_trace(net, trafos=net.trafo.index, color="black", trace_name="transformer")
    # feeder's trace
    ft = plot.plotly.create_bus_trace(net, net.ext_grid.bus.values, patch_type="square", size=15, color="yellow",
                                      trace_name="feeder")

    # buses over 1.1 pu trace
    high_voltage_buses = net.res_bus[net.res_bus.vm_pu > 1.1].index
    hvbt = plot.plotly.create_bus_trace(net, high_voltage_buses, size=10, color="red", trace_name="Voltage over 1.1 pu")

    plot.plotly.draw_traces(lt + tt + bt + hvbt + ft, figsize=1)


def trace_figure_colored(net):
    plot.create_generic_coordinates(net)
    # lines' trace
    lt = plot.plotly.create_line_trace(net, cmap=True, cmin=0, cmax=100, cbar_title="Line loading [%]", width=2)
    # buses' trace
    bt = plot.plotly.create_bus_trace(net, cmap=True, cbar_title="Bus voltage [pu]", size=10)
    # transformer's trace
    tt = plot.plotly.create_trafo_trace(net, trafos=net.trafo.index, color="black", trace_name="transformer", width=3)

    plot.plotly.draw_traces(lt + bt + tt, showlegend=False, aspectratio=(20, 7))
