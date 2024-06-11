#!/usr/bin/env python3
"""
Convert cell morphology to NeuroML.

We only export morphologies here. We add the biophysics manually.

File: NeuroML2/cellmorph2nml.py
"""

import os

import neuroml
import pyneuroml
from neuron import h
from pyneuroml.io import read_neuroml2_file, write_neuroml2_file
from pyneuroml.neuron import export_to_neuroml2


def main(acell):
    """Main runner method.

    :param acell: name of cell
    :returns: None

    """
    neuroml_morph_export_file = f"{acell}.morph.export.cell.nml"
    neuroml_morph_file = f"{acell}.morph.cell.nml"
    loader_hoc_file = f"{acell}_loader.hoc"
    loader_hoc_file_txt = """
    load_file("stdrun.hoc")

    xopen("../NEURON/Purkinje19b972-1.nrn") // Load the morphology file.
    forsec "axon" delete_section()  // Delete original axon and add a fake AIS
    """

    with open(loader_hoc_file, "w") as f:
        print(loader_hoc_file_txt, file=f)

    export_to_neuroml2(
        loader_hoc_file,
        neuroml_morph_export_file,
        includeBiophysicalProperties=False,
        validate=False,
    )

    os.remove(loader_hoc_file)

    # extract only the cell from the exported file
    neuroml_document = read_neuroml2_file(neuroml_morph_export_file)
    purkinje_cell = neuroml_document.cells[0]
    purkinje_cell.id = "Purkinje_cell"
    purkinje_cell.notes += """
Original model:
Zang, Y.; Dieudonné, S. &
Schutter, E. D. Voltage- and Branch-Specific Climbing Fiber Responses in
Purkinje Cells Cell Reports, Elsevier BV, 2018, 24, 1536-1549

https://doi.org/10.1016/j.celrep.2018.07.011
    """
    new_document = neuroml.NeuroMLDocument(id="ZangEtAl2018_Purkinje_cell")
    new_document.add(purkinje_cell)
    write_neuroml2_file(new_document, neuroml_morph_file, validate=True)

    print(
        f"Cell exported. Try visualising it with `pynml-plotmorph -i {neuroml_morph_file}`"
    )


if __name__ == "__main__":
    main("Purkinje")
