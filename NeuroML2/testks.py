#!/usr/bin/env python3
"""
Generate scripts to test KS channels.

Since we don't currently have the protocol implemented for the NeuroML
channels.

File: testks.py

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import typing
import neuroml
from neuroml.utils import component_factory
from pyneuroml.io import write_neuroml2_file
from pyneuroml.lems import generate_lems_file_for_neuroml


def generate_ks_mod(channel_file):
    """Generate script for KS channel mod file

    :param channel_file: TODO
    :returns: TODO

    """
    pass


def generate_ks_nml(channel_file):
    """Generate script for KS channel NML file

    :param channel_file: TODO
    :returns: TODO

    """
    newdoc = component_factory(neuroml.NeuroMLDocument, id="testdoc")
    typing.reveal_type(newdoc)
    newcell = newdoc.add(neuroml.Cell, id="testcell", validate=False)  # type: neuroml.Cell
    typing.reveal_type(newcell)
    newcell.setup_nml_cell()
    newcell.set_spike_thresh("10mV")

    newcell.add_segment(prox=[0, 0, 0, 5], dist=[10, 0, 0, 5], name="soma0",
                        seg_type="soma", seg_id="0", use_convention=True)

    newcell.add_channel_density(newdoc, cd_id="pas", ion_channel="pas", ion="non_specific",
                                group_id="all", erev="-65mV",
                                cond_density="0.001 S_per_cm2",
                                ion_chan_def_file="channels/pas.channel.nml")
    newcell.morphinfo(True)
    newcell.biophysinfo()

    newnet = newdoc.add(neuroml.Network, id="testdoc", validate=False)
    newpop = newnet.add(neuroml.Population, id="testpop", component=newcell.id,
                        size=1)

    newdoc.validate(recursive=True)
    write_neuroml2_file(newdoc, "TestKS.net.nml")


    generate_lems_file_for_neuroml(sim_id="testsim",
                                   neuroml_file="TestKS.net.nml",
                                   target=newnet.id, duration="1000ms",
                                   dt="0.01ms",
                                   lems_file_name="LEMS_testks.xml",
                                   nml_doc=newdoc, target_dir=".")


if __name__ == "__main__":
    generate_ks_nml("something")
