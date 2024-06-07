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


def annotate_SK2():
    """Annotation for SK2 channel"""
    annotation = create_annotation(
        subject="SK2",
        title="NeuroML conversion of SK2 channel from Zang et al",
        abstract=None,
        serialization_format="pretty-xml",
        annotation_style="miriam",
        indent=12,
        xml_header=False,
        description="SK type Ca2+ dependent K+ channel (After HyperPolarizing)",
        creation_date="2019-12-09",
        modified_dates=["2024-06-05"],
        citations={"https://doi.org/10.3389/neuro.03.002.2007": "Journal of Neuroscience"},
        sources={"https://modeldb.science/243446": "modeldb",
                 "https://github.com/ModelDBRepository/243446": "GitHub"},
        authors={
            "Sergio Solinas": {},
            "Lia Forti": {},
            "Egidio D'Angelo": {},
        },
        contributors={
            "Padraig Gleeson": {"https://orcid.org/0000-0001-5963-8576": "orcid"},
            "Ankur Sinha": {"https://orcid.org/0000-0001-7568-7167": "orcid"},
        },
        is_part_of={"http://uri.neuinfo.org/nif/nifstd/sao471801888": "purkinje cell"},
        predecessors={
            "https://modeldb.science/80769": "Original model",
            "https://github.com/OpenSourceBrain/SolinasEtAl-GolgiCell/blob/master/NeuroML2/Golgi_KAHP.channel.nml": "GitHub",
        },
        see_also={"https://doi.org/10.1085/jgp.111.4.565": "Data from"}
    )
    print(annotation)

def annotate_mslo():
    """Annotation for mslo channel"""
    annotation = create_annotation(
        subject="Kmslo",
        title="NeuroML conversion of mslo channel from Zang et al",
        abstract=None,
        serialization_format="pretty-xml",
        annotation_style="miriam",
        indent=12,
        xml_header=False,
        description="Large conductance Ca2+ activated K+ channel mslo",
        is_={"http://uri.neuinfo.org/nif/nifstd/nifext_2511": "Voltage-gated potassium channel"},
        creation_date="2024-06-07",
        citations={"https://doi.org/10.1007/s12311-010-0224-3": "Cerebellum"},
        sources={"https://modeldb.science/243446": "modeldb",
                 "https://github.com/ModelDBRepository/243446": "GitHub"},
        authors={
            "Ankur Sinha": {"https://orcid.org/0000-0001-7568-7167": "orcid"},
        },
        is_part_of={"http://uri.neuinfo.org/nif/nifstd/sao471801888": "purkinje cell"},
        see_also={"https://doi.org/10.1046/j.1460-9568.2002.02171.x": "Data from"}
    )
    print(annotation)


if __name__ == "__main__":
    annotate_mslo()
