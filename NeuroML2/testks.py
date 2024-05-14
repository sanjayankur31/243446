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
    newcell = newdoc.add(neuroml.Cell, id="testcell", validate=False)
    typing.reveal_type(newcell)
    newcell.setup_nml_cell()
    newcell.set_spike_thresh("10mV")


if __name__ == "__main__":
    generate_ks_nml("something")
