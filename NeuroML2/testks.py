#!/usr/bin/env python3
"""
Generate scripts to test KS channels.

Since we don't currently have the protocol implemented for the NeuroML
channels.

File: testks.py

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import neuroml
import subprocess
from neuroml.utils import component_factory
from pyneuroml.io import write_neuroml2_file
from pyneuroml.lems import generate_lems_file_for_neuroml
from pyneuroml.runners import run_lems_with_jneuroml_neuron
from pyneuroml.plot import generate_plot
import neuron


def test_channel_mod(channel, amplitude):
    """Generate script for KS channel mod file

    :param channel_file: TODO
    :returns: TODO

    """
    h = neuron.h
    h.celsius = 34
    h.load_file("stdrun.hoc")
    h(
        """
    objref p
    p = new PythonObject()
    """
    )
    # Create a section, set size & insert pas, passive channel mechanism
    soma = h.Section(name="soma")

    soma.L = 10
    soma.nseg = 1
    for seg in soma:
        soma.diam = 5

    soma.insert("pas")
    soma(0.5).g_pas = 0.001
    soma(0.5).e_pas = -65

    try:
        soma.insert(str(channel))
    except ValueError:
        try:
            subprocess.run(args=["nrnivmodl", "mod"], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            return 1
        h.nrn_load_dll("x86_64/.libs/libnrnmech.so")
        soma.insert(str(channel))


    # recording
    vRec = h.Vector().record(soma(0.5)._ref_v)
    tRec = h.Vector().record(h._ref_t)

    ic = h.IClamp(soma(0.5))
    ic.delay = 200
    ic.dur = 1000
    ic.amp = float(amplitude)
    v0 = -0.5  # Pre holding potential

    h.finitialize(v0)
    h.dt = 0.01
    h.continuerun(1200)

    print(tRec.to_python())
    generate_plot(xvalues=[tRec.to_python()], yvalues=[vRec.to_python()],
                  title="memb (neuron)", labels=["v"], show_plot_already=True)


def test_channel_nml(channel=None, ion=None, erev=None, amplitude="0.07 nA",
                     record_data={}):
    """Generate script for KS channel NML file

    :param channel: TODO
    :returns: TODO

    """
    newdoc = component_factory(neuroml.NeuroMLDocument, id="testdoc")

    newcell = newdoc.add(neuroml.Cell, id="testcell", validate=False)  # type: neuroml.Cell
    newcell.setup_nml_cell()
    newcell.set_spike_thresh("10mV")

    newcell.add_segment(prox=[0, 0, 0, 5], dist=[10, 0, 0, 5], name="soma0",
                        seg_type="soma", seg_id="0", use_convention=True)

    # add passive
    newcell.add_channel_density(newdoc, cd_id="pas", ion_channel="pas", ion="non_specific",
                                group_id="all", erev="-65mV",
                                cond_density="0.001 S_per_cm2",
                                ion_chan_def_file="channels/pas.channel.nml")

    if channel:
        newcell.add_channel_density(newdoc, cd_id=channel, ion_channel=channel,
                                    ion=ion,
                                    group_id="all", erev=erev,
                                    cond_density="0.001 S_per_cm2",
                                    ion_chan_def_file=f"channels/{channel}.channel.nml")
    else:
        channel = "pas"

    newcell.morphinfo(True)
    newcell.biophysinfo()

    newnet = newdoc.add(neuroml.Network, id="testdoc", validate=False,
                        temperature="34 degC")
    newpop = newnet.add(neuroml.Population, id="testpop", component=newcell.id,
                        size=1)

    # Define an external stimulus and add it to the model
    pg = newdoc.add(
        "PulseGenerator",
        id="pulseGen_0", delay="200ms", duration="1000ms",
        amplitude=amplitude
    )
    exp_input = newnet.add("ExplicitInput", target="%s[%i]" % (newpop.id, 0), input=pg.id)

    newdoc.validate(recursive=True)
    write_neuroml2_file(newdoc, f"Test_{channel}.net.nml")

    generate_lems_file_for_neuroml(sim_id=f"testsim_{channel}",
                                   neuroml_file=f"Test_{channel}.net.nml",
                                   target=newnet.id, duration="1200ms",
                                   dt="0.01ms",
                                   lems_file_name=f"LEMS_test_{channel}.xml",
                                   nml_doc=newdoc, target_dir=".",
                                   gen_saves_for_all_v=True,
                                   gen_saves_for_quantities={},
                                   include_extra_files=[f"channels/{channel}.channel.nml"])

    data = run_lems_with_jneuroml_neuron(f"LEMS_test_{channel}.xml", nogui=True,
                                         load_saved_data=True,
                                         show_plot_already=False)
    keys = list(data.keys())
    print(f"Recorded data: {data.keys()}")

    generate_plot(xvalues=[data[keys[0]]], yvalues=[data[keys[1]]],
                  title="Memb pot", labels=["v"], show_plot_already=True)


if __name__ == "__main__":
    test_channel_mod(
        channel="narsg", amplitude=0.1)
    """

    test_channel_nml(
        channel="NaRSG", ion="na", erev="67 mV", amplitude="0.1 nA",
        record_data={})
    """
