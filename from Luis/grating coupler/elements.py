from technologies import silicon_photonics
from ipkiss3 import all as i3
from picazzo3.traces.wire_wg import WireWaveguideTemplate
from picazzo3.fibcoup.uniform import UniformLineGrating
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear
from picazzo3.routing.place_route import PlaceComponents
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.wg.spirals import DoubleSpiralWithInCouplingRounded
from picazzo3.filters.ring import RingRectNotchFilter
from picazzo3.filters.ring import RingRect180DropFilter
from picazzo3.filters.ring import RingRectWrappedNotchFilter
from picazzo3.filters.ring import RingRectWrapped180DropFilter


# def gratingwaveguide(w_core, w_ebeam=1.5):
#     # w_core [int] -> waveguide width
#     # w_clad [int] -> cladding width
#     # w_ebeam [int] -> ebeam beam width
#     w_clad = 8.0
#     w_core = w_core + w_ebeam
#     w_clad = w_core - 2 * w_ebeam + 2 * w_clad
#     wg = WireWaveguideTemplate()
#     wg.Layout(core_width=w_core, cladding_width=w_clad)
#
#     return wg

def gratingwaveguide(w_core, w_ebeam=4):
    # w_core [int] -> waveguide width
    # w_ebeam [int] -> ebeam beam width

    w_core = w_core + w_ebeam
    w_clad = w_core + 2 * w_ebeam
    wg = WireWaveguideTemplate()
    wg.Layout(core_width=w_core, cladding_width=w_clad)

    return wg


def FBMSwaveguide(w_core, l_core, w_ebeam=4):
    # w_core [int] -> waveguide width
    # l_core [int] -> waveguide length
    # w_ebeam [int] -> ebeam beam width

    w_core = w_core + w_ebeam
    w_clad = w_core + 2 * w_ebeam
    wgt = WireWaveguideTemplate()
    wgt.Layout(core_width=w_core, cladding_width=w_clad)
    # wg = wgt()
    wg = i3.Waveguide(trace_template=wgt)
    wg.Layout(shape=[(0, 0), (l_core, 0)])

    return (wgt, wg)


def grating(wg, l, p, dc, pos=0):
    # wg [wg] -> waveguide template to place the grating
    # l [int] -> socket length inside the waveguide to draw the grating
    # p [int] -> grating period length
    # dc [0-1] -> grating duty cycle
    FGC = UniformLineGrating(trace_template=wg)
    FGC.Layout(period=p, line_width=p * (1 - dc),
               line_length=wg.Layout.view.core_width + 1,
               n_o_periods=int(l * 9/ 10 // p), socket_length=l)

    return FGC


def taper(wg1, wg2, l):
    # wg1 [wg] -> waveguide to connect on one side
    # wg2 [wg] -> waveguide to connect on the other side
    # l [int] -> length of the taper

    t = WireWaveguideTransitionLinear(start_trace_template=wg1,
                                      end_trace_template=wg2)
    t.Layout(start_position=(0, 0), end_position=(l, 0))

    return t


def FBMSwaveguidecircuit(wg_length, wg_width, taper_length, grating_wg_width,
                         grating_socket_length, grating_period, grating_dc):
    # wg_length [int] -> waveguide length
    # wg_width [int] -> waveguide width
    # taper_length [int] -> taper length
    # grating_wg_width [int] -> width of the waveguide for the grating
    # grating_socket_length [int] -> grating socket length
    # grating_period [int] -> grating period
    # grating_dc [0-1] -> grating duty cycle

    gwg = gratingwaveguide(grating_wg_width)
    g = grating(gwg, grating_socket_length, grating_period, grating_dc)
    (wgt, wg) = FBMSwaveguide(wg_width, wg_length)
    t = taper(gwg, wgt, taper_length)

    circuit = PlaceAndAutoRoute(child_cells={"grating1": g,
                                             "taper1": t,
                                             "wire": wg,
                                             "taper2": t,
                                             "grating2": g})

    circuit_layout = circuit.get_default_view(i3.LayoutView)
    circuit_layout.set(
        child_transformations={
            "grating1": i3.Translation(
                (g.Layout.view.socket_length / 2, 0)),
            "taper1": i3.Translation((g.Layout.view.socket_length,
                                      0)),
            "wire": i3.Translation((g.Layout.view.socket_length +
                                    t.Layout.view.end_position[0], 0)),
            "taper2": i3.Rotation(rotation_center=(0.0, 0.0),
                                  rotation=180,
                                  absolute_rotation=False) +
                      i3.Translation((g.Layout.view.socket_length +
                                      2 * t.Layout.view.end_position[0] +
                                      wg.Layout.view.shape[1][0], 0)),
            "grating2": i3.Rotation(rotation_center=(0.0, 0.0),
                                    rotation=180,
                                    absolute_rotation=False) +
                        i3.Translation((g.Layout.view.socket_length * 3 / 2 +
                                        2 * t.Layout.view.end_position[0] +
                                        wg.Layout.view.shape[1][0], 0))})

    # circuit_layout = circuit.Layout(
    #     child_transformations={
    #         "grating1": i3.Translation(
    #             (g.Layout.view.socket_length / 2, 0)),
    #         "taper1": i3.Translation((g.Layout.view.socket_length,
    #                                   0)),
    #         "wire": i3.Translation((g.Layout.view.socket_length +
    #                                 t.Layout.view.end_position[0], 0)),
    #         "taper2": i3.Rotation(rotation_center=(0.0, 0.0),
    #                               rotation=180,
    #                               absolute_rotation=False) +
    #                   i3.Translation((g.Layout.view.socket_length +
    #                                   2 * t.Layout.view.end_position[0] +
    #                                   wg.Layout.view.shape[1][0], 0)),
    #         "grating2": i3.Rotation(rotation_center=(0.0, 0.0),
    #                                 rotation=180,
    #                                 absolute_rotation=False) +
    #                     i3.Translation((g.Layout.view.socket_length * 3 / 2 +
    #                                     2 * t.Layout.view.end_position[0] +
    #                                     wg.Layout.view.shape[1][0], 0))})

    return circuit


def waveguidecircuit(wg_length, w_core, w_clad, taper_length, grating_wg_width,
                     grating_socket_length, grating_period, grating_dc):
    # wg_length [int] -> waveguide length
    # wg_width [int] -> waveguide width
    # taper_length [int] -> taper length
    # grating_wg_width [int] -> width of the waveguide for the grating
    # grating_socket_length [int] -> grating socket length
    # grating_period [int] -> grating period
    # grating_dc [0-1] -> grating duty cycle

    wgt = WireWaveguideTemplate()
    wgt.Layout(core_width=w_core, cladding_width=w_clad)
    wg = wgt()
    wg.Layout(shape=[(0, 0), (wg_length, 0)])
    gwg = gratingwaveguide(grating_wg_width)
    g = grating(gwg, grating_socket_length, grating_period, grating_dc)
    t = taper(gwg, wgt, taper_length)

    circuit = PlaceAndAutoRoute(child_cells={"grating1": g,
                                             "taper1": t,
                                             "wire": wg,
                                             "taper2": t,
                                             "grating2": g})

    circuit_layout = circuit.Layout(
        child_transformations={
            "grating1": i3.Translation(
                (grating_socket_length / 2, 0)),
            "taper1": i3.Translation((grating_socket_length, 0)),
            "wire": i3.Translation((grating_socket_length +
                                    taper_length, 0)),
            "taper2": i3.Rotation(rotation_center=(0.0, 0.0),
                                  rotation=180,
                                  absolute_rotation=False) +
                      i3.Translation((grating_socket_length +
                                      2 * taper_length + wg_length, 0)),
            "grating2": i3.Rotation(rotation_center=(0.0, 0.0),
                                    rotation=180,
                                    absolute_rotation=False) +
                        i3.Translation((grating_socket_length * 3 / 2 +
                                        2 * taper_length + wg_length, 0))})

    return circuit


def spiral(wgw, n_loop, inner_size, spacing, incoupling_length, w_ebeam=4):
    w_core = wgw + w_ebeam
    w_clad = wgw + 3 * w_ebeam
    wgt = WireWaveguideTemplate()
    wgt.Layout(core_width=w_core, cladding_width=w_clad)

    s = DoubleSpiralWithInCouplingRounded(n_o_loops=n_loop,
                                          trace_template=wgt)
    sl = s.Layout(angle_step=30, inner_size=inner_size,
                  incoupling_length=incoupling_length,
                  bend_radius=300,
                  manhattan=False,
                  spacing=spacing)

    print(sl.trace_length())

    return s


def spiralcircuit(wgw, nl, i_s, s, il, tl, gwgw, gsl, gp, gdc, w_ebeam=4):
    # wgw [int] -> waveguide width
    # nl -> Number of loops in the spiral
    # i_s -> inner size of the spiral coordinate2
    # s -> spacing between the individual loops
    # il -> incoupling length
    # tl -> taper length
    # gwgw = 10  # width of the waveguide for the grating
    # gsl = 78  # grating socket length
    # gp = 2.3  # grating period length
    # gdc = [0-1] -> grating duty cycle
    w_core = wgw + w_ebeam
    w_clad = wgw + 3 * w_ebeam
    gwg = gratingwaveguide(gwgw)
    g = grating(gwg, gsl, gp, gdc)
    sp = spiral(wgw, nl, i_s, s, il)
    wgt = WireWaveguideTemplate()
    wgt.Layout(core_width=w_core, cladding_width=w_clad)
    t = taper(gwg, wgt, tl)

    circuit = PlaceAndAutoRoute(child_cells={"grating1": g,
                                             "taper1": t,
                                             "spiral": sp,
                                             "taper2": t,
                                             "grating2": g})
    print i_s[0]
    circuit_layout = circuit.Layout(
        child_transformations={
            "grating1": i3.Translation(
                (gsl / 2, 0)),
            "taper1": i3.Translation((gsl, 0)),
            "spiral": i3.Translation((gsl + tl, 0)),
            "taper2": i3.Rotation(rotation_center=(0.0, 0.0),
                                  rotation=180,
                                  absolute_rotation=False) +
                      # i3.Translation((
                      #     gsl + 2 * tl + i_s[0] + (4 * nl + 1) * s + 2 * il, 0)),
                      i3.Translation((
                          gsl + 2 * tl + i_s[0] + 4 * (nl-1) * s + 300 + 2 * il, 0)),

            "grating2": i3.Rotation(rotation_center=(0.0, 0.0),
                                    rotation=180,
                                    absolute_rotation=False) +
                        i3.Translation((
                            gsl * 3 / 2 + 2 * tl + i_s[0] + 4 * (nl-1) * s + 300 + 2 * il, 0))})

    return circuit


def ring1(radius, gap, wg_ring_width, wg_coupler_width):
    gap2 = gap + wg_ring_width / 2.0 + wg_coupler_width / 2.0
    wg_ring = WireWaveguideTemplate()
    wg_coupler = WireWaveguideTemplate()
    wg_ring.Layout(
        core_width=wg_ring_width, cladding_width=wg_ring_width + 6)
    wg_coupler.Layout(
        core_width=wg_coupler_width, cladding_width=wg_coupler_width + 6)

    ring = RingRectNotchFilter(ring_trace_template=wg_ring,
                               coupler_trace_templates=[wg_coupler])
    ring_layout = ring.Layout(angle_step=0.1, bend_radius=radius,
                              coupler_spacings=[gap2], straights=(0, 0),
                              coupler_extensions=[i3.Coord2((20, 20))])

    return ring


def ringcircuit1(radius, gap, wg_ring_width, wg_coupler_width,
                 tl, gwgw, gsl, gp, gdc):
    gwg = gratingwaveguide(gwgw)
    g = grating(gwg, gsl, gp, gdc)
    r = ring1(radius, gap, wg_ring_width, wg_coupler_width)
    wgt = WireWaveguideTemplate()
    wgt.Layout(core_width=wg_coupler_width,
               cladding_width=wg_coupler_width + 6)
    t = taper(gwg, wgt, tl)

    circuit = PlaceAndAutoRoute(child_cells={"grating1": g,
                                             "taper1": t,
                                             "ring": r,
                                             "taper2": t,
                                             "grating2": g})

    circuit_layout = circuit.Layout(
        child_transformations={
            "grating1": i3.Translation((gsl / 2.0, 0)),
            "taper1": i3.Translation((gsl, 0)),
            "ring": i3.Translation((gsl + tl + 20,
                                    radius + gap + wg_ring_width / 2.0 +
                                    wg_coupler_width / 2.0)),
            "taper2": i3.Rotation(rotation_center=(0.0, 0.0),
                                  rotation=180,
                                  absolute_rotation=False) +
                      i3.Translation((gsl + 2 * tl + 40, 0)),
            "grating2": i3.Rotation(rotation_center=(0.0, 0.0),
                                    rotation=180,
                                    absolute_rotation=False) +
                        i3.Translation((gsl * 3 / 2.0 + 2 * tl + 40, 0))})

    return circuit


def ring2(radius, gap, gap1, wg_ring_width, wg_coupler_width, wg_coupler_width2):
    gap2 = gap + wg_ring_width / 2.0 + wg_coupler_width / 2.0
    gap3 = gap1 + wg_ring_width / 2.0 + wg_coupler_width / 2.0
    wg_ring = WireWaveguideTemplate()
    wg_coupler = WireWaveguideTemplate()
    wg_ring.Layout(
        core_width=wg_ring_width, cladding_width=wg_ring_width + 6)
    wg_coupler.Layout(
        core_width=wg_coupler_width, cladding_width=wg_coupler_width + 6)
    wg_coupler2 = WireWaveguideTemplate()
    wg_coupler2.Layout(
        core_width=wg_coupler_width2, cladding_width=wg_coupler_width2 + 6)

    ring = RingRect180DropFilter(ring_trace_template=wg_ring,
                                 coupler_trace_templates=[wg_coupler, wg_coupler2])
    ring_layout = ring.Layout(angle_step=0.1, bend_radius=radius,
                              coupler_spacings=[gap2, gap3], straights=(0, 0),
                              coupler_extensions=[i3.Coord2((20, 20)),
                                                  i3.Coord2((20, 20))])

    return ring


def ringcircuit2(radius, gap, gap1, wg_ring_width,
                 wg_coupler_width, wg_coupler_width2,
                 tl, gwgw, gsl, gp, gdc, gp2, gdc2):
    gwg = gratingwaveguide(gwgw)
    g = grating(gwg, gsl, gp, gdc)
    g2 = grating(gwg, gsl, gp2, gdc2)
    r = ring2(radius, gap, gap1, wg_ring_width, wg_coupler_width, wg_coupler_width2)
    wgt = WireWaveguideTemplate()
    wgt.Layout(core_width=wg_coupler_width,
               cladding_width=wg_coupler_width + 6)
    wgt2 = WireWaveguideTemplate()
    wgt2.Layout(core_width=wg_coupler_width2,
                cladding_width=wg_coupler_width2 + 6)
    t = taper(gwg, wgt, tl)
    t2 = taper(gwg, wgt2, tl)

    circuit = PlaceAndAutoRoute(child_cells={"grating1": g,
                                             "taper1": t,
                                             "ring": r,
                                             "taper2": t,
                                             "grating2": g,
                                             "grating3": g2,
                                             "taper3": t2,
                                             "taper4": t2,
                                             "grating4": g2})

    circuit_layout = circuit.Layout(
        child_transformations={
            "grating1": i3.Translation((gsl / 2.0, 0)),
            "taper1": i3.Translation((gsl, 0)),
            "ring": i3.Translation((gsl + tl + 20,
                                    radius + gap + wg_ring_width / 2.0 +
                                    wg_coupler_width / 2.0)),
            "taper2": i3.Rotation(rotation_center=(0.0, 0.0),
                                  rotation=180,
                                  absolute_rotation=False) +
                      i3.Translation((gsl + 2 * tl + 40, 0)),
            "grating2": i3.Rotation(rotation_center=(0.0, 0.0),
                                    rotation=180,
                                    absolute_rotation=False) +
                        i3.Translation((gsl * 3 / 2.0 + 2 * tl + 40, 0)),
            "grating3": i3.Translation((gsl / 2.0, 2 * radius + gap + gap1 + wg_ring_width + wg_coupler_width)),
            "taper3": i3.Translation((gsl, 2 * radius + gap + gap1 + wg_ring_width + wg_coupler_width)),
            "taper4": i3.Rotation(rotation_center=(0.0, 0.0),
                                  rotation=180,
                                  absolute_rotation=False) +
                      i3.Translation((gsl + 2 * tl + 40, 2 * radius + gap + gap1 + wg_ring_width + wg_coupler_width)),
            "grating4": i3.Rotation(rotation_center=(0.0, 0.0),
                                    rotation=180,
                                    absolute_rotation=False) +
                        i3.Translation(
                            (gsl * 3 / 2.0 + 2 * tl + 40, 2 * radius + gap + gap1 + wg_ring_width + wg_coupler_width))})

    return circuit


def ring3(radius, gap, wg_ring_width, wg_coupler_width, angle):
    gap2 = gap + wg_ring_width / 2.0 + wg_coupler_width / 2.0
    wg_ring = WireWaveguideTemplate()
    wg_coupler = WireWaveguideTemplate()
    wg_ring.Layout(
        core_width=wg_ring_width, cladding_width=wg_ring_width + 6)
    wg_coupler.Layout(
        core_width=wg_coupler_width, cladding_width=wg_coupler_width + 6)

    ring = RingRectWrappedNotchFilter(ring_trace_template=wg_ring,
                                      coupler_trace_templates=[wg_coupler])
    ring_layout = ring.Layout(angle_step=0.1, bend_radius=radius,
                              coupler_spacings=[gap2], straights=(0, 0),
                              coupler_lengths=[0],
                              coupler_angles=[angle, angle])

    return ring


def ringcircuit3(radius, gap, wg_ring_width, wg_coupler_width, angle, lx, ly,
                 tl, gwgw, gsl, gp, gdc):
    gwg = gratingwaveguide(gwgw)
    g = grating(gwg, gsl, gp, gdc)
    r = ring3(radius, gap, wg_ring_width, wg_coupler_width, angle)
    wgt = WireWaveguideTemplate()
    wgt.Layout(core_width=wg_coupler_width,
               cladding_width=wg_coupler_width + 6)
    t = taper(gwg, wgt, tl)

    circuit = PlaceAndAutoRoute(child_cells={"grating1": g,
                                             "taper1": t,
                                             "ring": r,
                                             "taper2": t,
                                             "grating2": g})

    circuit_layout = circuit.Layout(
        child_transformations={
            "grating1": i3.Translation((gsl / 2.0, ly)),
            "taper1": i3.Translation((gsl, ly)),
            "ring": i3.Translation((gsl + tl + lx / 2.0,
                                    radius + gap + wg_ring_width / 2.0 +
                                    wg_coupler_width / 2.0)),
            "taper2": i3.Rotation(rotation_center=(0.0, 0.0),
                                  rotation=180,
                                  absolute_rotation=False) +
                      i3.Translation((gsl + 2 * tl + lx, ly)),
            "grating2": i3.Rotation(rotation_center=(0.0, 0.0),
                                    rotation=180,
                                    absolute_rotation=False) +
                        i3.Translation((gsl * 3 / 2.0 + 2 * tl + lx, ly))})

    return circuit
