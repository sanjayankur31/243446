#!/usr/bin/env python3
"""
Script to create annotations for various models.

File: create_annotations.py

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


from pyneuroml.annotations import create_annotation


def annotate_Kv1():
    """Annotation for Kv1 channel"""
    annotation = create_annotation(
        subject="Kv1",
        title="NeuroML conversion of Kv1 channel from Zang et al",
        abstract=None,
        serialization_format="pretty-xml",
        annotation_style="miriam",
        indent=12,
        xml_header=False,
        description="Voltage-gated low threshold potassium current from Kv1 subunits",
        creation_date="2024-04-26",
        citations={"https://doi.org/10.1523/JNEUROSCI.5204-05.2006": "Journal of Neuroscience"},
        sources={"https://modeldb.science/243446?tab=1": "modeldb",
                 "https://github.com/ModelDBRepository/243446": "GitHub"},
        predecessors={"https://modeldb.science/80769": "Original model"},
        authors={"Walther Akemann": {"akemann at brain.riken.jp": "email"}},
        contributors={"Ankur Sinha": {"https://orcid.org/0000-0001-7568-7167": "orcid"}},
        is_part_of={"http://uri.neuinfo.org/nif/nifstd/sao471801888": "purkinje cell"},
    )
    print(annotation)

if __name__ == "__main__":
    annotate_Kv1()
