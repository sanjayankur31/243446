#!/usr/bin/env python3
"""
Add biophysics to Purkinje Cell

File: purkinje_cell.py

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


from neuroml.utils import component_factory
from pyneuroml.io import write_neuroml2_file


def pc_add_biophysics():
    """Add biophysics to Purkinje Cell
    :returns: TODO

    """
    doc = component_factory("NeuroMLDocument", id="ZangEtAl2018_Purkinje_cell_doc")
    # include purkinje cell morphology
    doc.add("IncludeType", href="Purkinje.morph.cell.nml")
    cell = doc.add("Cell", id="ZangEtAl2018_Purkinje_Cell",
                   morphology_attr="Purkinje_cell_morph", morphology=None)

    cell.morphology = None

    # TODO update component factory to not overwrite args for cell

    write_neuroml2_file(doc, "Purkinje.cell.nml")


if __name__ == "__main__":
    pc_add_biophysics()
